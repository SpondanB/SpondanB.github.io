---
myst:
  html_meta:
    "description": "KindaGPT: Understanding Transformers by building a small GPT-style language model from scratch in PyTorch — Spondan Bandyopadhyay"
---

# KindaGPT: Understanding Transformers by Building One From Scratch

**What actually happens inside a GPT model? Instead of treating Transformers as a black box, I decided to build a small one myself.**

:::{button-link} https://github.com/SpondanB/KindaGPT
:color: primary
:outline:
View Source on GitHub
:::
---

## 🎯 Why I Built KindaGPT

Large Language Models can sometimes feel almost magical.

Give a model a sequence of text and it can predict what comes next, maintain context, generate paragraphs, and seemingly understand relationships between words.

But underneath all of that are some surprisingly understandable building blocks.

I wanted to understand those building blocks rather than simply using something like:

```python
model = SomeExistingTransformer(...)
```

So I built **KindaGPT** — a small GPT-style language model from scratch using PyTorch.

The project intentionally avoids being a production-scale language model. The goal is much simpler:

> **Understand what is happening inside a Transformer by implementing its core components myself.**

The implementation includes token embeddings, positional embeddings, self-attention, multi-head attention, feed-forward networks, Transformer blocks, causal masking, and autoregressive text generation. 

And to understand why these pieces exist, the natural place to start is the paper that introduced the Transformer architecture:

**[Attention Is All You Need](https://arxiv.org/abs/1706.03762).**

---

## 🧠 Before Transformers: Why Attention?

Before the Transformer, sequence modelling was dominated by architectures involving **recurrent neural networks** and convolutional approaches.

The problem with recurrent models is intuitive.

Suppose we want to process:

```text
"The cat sat on the mat because it was tired."
```

A recurrent model processes the sequence step by step:

```text
The → cat → sat → on → the → mat → because → it → was → tired
```

Information has to travel through this chain.

Transformers introduced a fundamentally different approach.

Instead of requiring information to move sequentially from one token to the next, the model can allow tokens to **directly interact with other tokens through attention**.

The original paper proposed the Transformer as an architecture based entirely on attention mechanisms, removing recurrence and convolution from the core sequence-transduction architecture. The authors also highlighted the resulting increase in parallelizability during training. ([arXiv][1])

This is the idea that made the Transformer so interesting.

---

## 🔍 The Basic Idea of Attention

Let's take a simple sentence:

```text
"The animal didn't cross the street because it was tired."
```

What does **"it"** refer to?

A model needs to understand relationships between different parts of the sequence.

Attention gives the model a mechanism for asking:

> **"Which other tokens should I pay attention to when understanding this token?"**

Instead of treating every previous token equally, the model learns different weights for different tokens.

Conceptually:

```text
The animal didn't cross the street because it was tired.
                         ↑
                         │
                        "it"
                         │
                  ┌──────┴──────┐
                  │             │
                animal        street
                  ↑
             more relevant
```

The model learns these relationships rather than us explicitly programming them.

---

## 🧩 Queries, Keys and Values

The Transformer paper describes attention using three components:

* **Query (Q)**
* **Key (K)**
* **Value (V)**

A useful way to think about them is:

### Query

> **"What am I looking for?"**

### Key

> **"What information do I contain?"**

### Value

> **"What information should I provide if I'm relevant?"**

For every token, the model creates these three representations.

In KindaGPT this happens here:

```python
self.key = nn.Linear(n_embd, head_size, bias=False)
self.query = nn.Linear(n_embd, head_size, bias=False)
self.value = nn.Linear(n_embd, head_size, bias=False)
```

The input therefore gets transformed into:

```text
Input embedding
      │
      ├──→ Query
      │
      ├──→ Key
      │
      └──→ Value
```

---

## 📐 Scaled Dot-Product Attention

The central equation from *Attention Is All You Need* is:

$$
\text{Attention}(Q,K,V)
=
\text{softmax}
\left(
\frac{QK^T}{\sqrt{d_k}}
\right)V
$$

This looks complicated initially, but it can be broken into a few simple steps.

---

### 1. Compare Queries and Keys

First, we calculate:

$$
QK^T
$$

This gives us a measure of how compatible each query is with each key.

In KindaGPT:

```python
wei = q @ k.transpose(-2, -1)
```

The result is essentially an attention score matrix.

For a sequence of length `T`, the matrix looks conceptually like:

```text
             Token 1  Token 2  Token 3  Token 4
Token 1         x
Token 2         x        x
Token 3         x        x        x
Token 4         x        x        x        x
```

Each row represents a token asking:

> **"How relevant is every other token to me?"**

---

## ⚖️ Why Divide by $\sqrt{d_k}$?

The paper doesn't simply use: $QK^T$

It uses:

$$
\frac{QK^T}{\sqrt{d_k}}
$$

This scaling is important because as the dimensionality of the key vectors grows, the dot products can become large. Large values fed into softmax can produce very peaked distributions and make optimization more difficult.

The scaling keeps the values in a more manageable range before softmax. ([Attention Is All You Need][1])

In KindaGPT this appears as:

```python
wei = q @ k.transpose(-2, -1) * C**-0.5
```

which is equivalent to dividing by:

$$
\sqrt{C}
$$

where `C` is the embedding dimension used by that attention head.

---

## 🎯 Turning Scores Into Probabilities

The raw attention scores aren't probabilities yet.

We apply softmax:

```python
wei = F.softmax(wei, dim=-1)
```

Now each row represents a distribution of attention across the available tokens.

Conceptually:

```text
Token A
   │
   ├── Token A: 0.10
   ├── Token B: 0.20
   ├── Token C: 0.60
   └── Token D: 0.10
```

The model is effectively saying:

> "When processing Token A, Token C is particularly important."

---

## 💡 Finally: Use the Values

Once we have the attention weights, we use them to combine the value vectors:

$$
\text{Output} = \text{AttentionWeights} \times V
$$

In the code:

```python
out = wei @ v
```

So the complete process becomes:

```text
             Input
               │
       ┌───────┼───────┐
       ▼       ▼       ▼
       Q       K       V
       │       │       │
       └───┬───┘       │
           ▼           │
        Q × Kᵀ         │
           │           │
           ▼           │
        Scaling        │
           │           │
           ▼           │
        Softmax        │
           │           │
           ▼           │
     Attention Weights │
           │           │
           └─────┬─────┘
                 ▼
              × Values
                 │
                 ▼
              Output
```

That is the heart of the Transformer.

---

## 🚫 The Problem of Looking Into the Future

There is an important difference between the original Transformer architecture and GPT-style language modelling.

When generating text, the model shouldn't be allowed to see the future.

Suppose the training sequence is:

```text
The cat sat on the mat
```

When predicting:

```text
The cat sat ...
```

the model should be able to use:

```text
The
The cat
The cat sat
```

but not:

```text
on the mat
```

Otherwise, the model would have access to the answer.

---

## 🔒 Causal Self-Attention

KindaGPT therefore uses a **causal mask**.

The mask creates a lower-triangular attention matrix:

```text
           1   2   3   4
         ┌──────────────────
       1 │ y   n   n   n
       2 │ y   y   n   n
       3 │ y   y   y   n
       4 │ y   y   y   y
```

A token can attend to itself and previous tokens, but not future ones.

The implementation creates this mask using:

```python
self.register_buffer(
    'tril',
    torch.tril(torch.ones(block_size, block_size))
)
```

and applies it with:

```python
wei = wei.masked_fill(
    self.tril[:T, :T] == 0,
    float('-inf')
)
```

The `-inf` values effectively become zero probability after softmax.

The original Transformer paper similarly uses masking in the decoder to prevent a position from attending to subsequent positions, ensuring that predictions depend only on previously known outputs. ([Attention Is All You Need][1])

---

## 🧠 One Attention Head Isn't Enough

A single attention mechanism can learn relationships between tokens.

But there may be many different relationships worth learning simultaneously.

For example:

```text
"The dog chased the ball because it was moving."
```

Different attention patterns might capture:

```text
"It" → "dog"

"moving" → "ball"

"chased" → "dog"
```

Rather than forcing one attention mechanism to capture everything, Transformers use **multiple attention heads**.

---

## 🧩 Multi-Head Attention

The original Transformer introduced **Multi-Head Attention**.

Instead of calculating one attention function:

$$
Attention(Q,K,V)
$$

we calculate several attention functions in parallel:

$$
head_i =
Attention(QW_i^Q,KW_i^K,VW_i^V)
$$

and then concatenate them:

$$
MultiHead(Q,K,V)
=
Concat(head_1,\ldots,head_h)W^O
$$

The idea is simple:

> **Let different attention heads learn different relationships.**

KindaGPT uses four heads:

```python
Block(n_embd, num_heads=4)
```

The architecture looks like:

```text
                       Input
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Head 1           Head 2         Head 3       Head 4
          │              │              │            │
          └──────────────┴──────────────┴────────────┘
                         │
                    Concatenate
                         │
                         ▼
                    Projection
                         │
                         ▼
                       Output
```

This is one of the central ideas from the original Transformer architecture. ([Attention Is All You Need][1])

---

## 📍 But Attention Doesn't Know Position

There is another subtle problem.

Self-attention doesn't inherently know that:

```text
"dog bites man"
```

is different from:

```text
"man bites dog"
```

The same tokens exist in both sequences.

Their **order** matters.

Because the Transformer removes recurrence, it needs another way to inject information about token position. The original paper therefore introduced **positional encodings**, added to token embeddings. ([Attention Is All You Need][1])

---

## 📌 Positional Information

KindaGPT uses learned positional embeddings:

```python
self.position_embedding_table = nn.Embedding(
    block_size,
    n_embd
)
```

The model then combines:

```python
tok_embed = self.token_embedding_table(idx)

pos_embed = self.position_embedding_table(
    torch.arange(T, device=device)
)

x = tok_embed + pos_embed
```

So the representation becomes:

$$
x = TokenEmbedding + PositionEmbedding
$$

Conceptually:

```text
             "cat"
               │
               ▼
        Token Embedding
               │
               +
               │
        Position Embedding
               │
               ▼
        Final Representation
```

The original paper used sinusoidal positional encodings, while also reporting experiments with learned positional embeddings. KindaGPT chooses the learned version because it is straightforward to implement for a small model. ([Attention Is All You Need][1])

---

## 🏗️ Building a Transformer Block

Now we have most of the pieces.

A Transformer block combines:

1. Self-attention
2. Feed-forward computation
3. Residual connections
4. Layer normalization

KindaGPT implements:

```python
x = x + self.sa_heads(self.ln1(x))

x = x + self.ffwd(self.ln2(x))
```

This can be visualized as:

```text
                Input
                  │
                  ├──────────────────┐
                  │                  │
                  ▼                  │
             LayerNorm               │
                  │                  │
                  ▼                  │
          Multi-Head Attention       │
                  │                  │
                  ▼                  │
                  + ◄────────────────┘
                  │
                  ├──────────────────┐
                  │                  │
                  ▼                  │
             LayerNorm               │
                  │                  │
                  ▼                  │
          Feed-Forward Network       │
                  │                  │
                  ▼                  │
                  + ◄────────────────┘
                  │
                  ▼
                Output
```

---

## 🔁 Why Residual Connections?

The `+ x` operations are **residual connections**.

Instead of forcing a layer to completely transform its input, we allow it to learn an adjustment:

$$
Output = x + F(x)
$$

This creates a direct path for information and gradients through the network.

The original Transformer surrounds its attention and feed-forward sub-layers with residual connections and normalization. ([Attention Is All You Need][1])

KindaGPT follows the same broad structure, although the exact normalization arrangement differs from the original paper's formulation.

---

## 🧮 The Feed-Forward Network

Attention is responsible for **communication between tokens**.

The feed-forward network then performs additional computation on each token representation.

KindaGPT implements:

```python
self.net = nn.Sequential(
    nn.Linear(n_embd, 4 * n_embd),
    nn.ReLU(),
    nn.Linear(4 * n_embd, n_embd),
)
```

With:

```text
32 → 128 → 32
```

This follows the general Transformer idea of a position-wise feed-forward network that expands the representation and then projects it back down. The original paper used a two-layer feed-forward network inside each Transformer layer. ([Attention Is All You Need][1])

A useful mental model is:

```text
Attention:
"Which information should I communicate with?"

Feed Forward:
"What computation should I perform on that information?"
```

---

## 🧱 Stacking Transformer Blocks

A single Transformer block is useful.

But the real power comes from stacking multiple blocks.

KindaGPT uses:

```python
self.blocks = nn.Sequential(
    Block(n_embd, num_heads=4),
    Block(n_embd, num_heads=4),
    Block(n_embd, num_heads=4),
    nn.LayerNorm(n_embd),
)
```

So the model becomes:

```text
Input
  │
  ▼
Transformer Block 1
  │
  ▼
Transformer Block 2
  │
  ▼
Transformer Block 3
  │
  ▼
LayerNorm
  │
  ▼
Language Model Head
```

The original Transformer similarly builds its architecture by stacking repeated layers; the paper's original encoder and decoder each used six layers. KindaGPT intentionally uses only three because the purpose here is understanding rather than scale. ([Attention Is All You Need][1])

---

## 🔤 From Characters to Embeddings

Before any of this happens, we need to turn text into numbers.

KindaGPT uses **character-level tokenization**.

For example:

```text
"hello"
```

becomes something conceptually like:

```text
[7, 4, 11, 11, 14]
```

The actual numbers depend on the vocabulary generated from `input.txt`.

The vocabulary is created using:

```python
chars = sorted(list(set(text)))
vocab_size = len(chars)
```

and mappings:

```python
stoi = {ch:i for i,ch in enumerate(chars)}
itos = {i:ch for i,ch in enumerate(chars)}
```

This makes the project deliberately simple.

There is no BPE tokenizer.

No WordPiece.

No subword vocabulary.

Just characters.

That makes the model less practical, but much easier to understand.

---

## 📦 Creating Training Examples

The text is split into:

```text
90% → Training
10% → Validation
```

and KindaGPT uses:

```python
block_size = 8
```

to create short contexts.

Suppose the sequence is:

```text
"hello world"
```

The model could receive:

```text
Input:
h e l l o

Target:
e l l o [next]
```

In other words:

> **Given everything I have seen so far, what character should come next?**

This is the fundamental training objective behind autoregressive language modelling.

---

## 🎯 Predicting the Next Token

After passing through the Transformer blocks, the representation reaches:

```python
self.lm_head = nn.Linear(n_embd, vocab_size)
```

This converts the embedding into a score for every possible character.

If the vocabulary contains 50 characters:

```text
Embedding
   │
   ▼
Linear Layer
   │
   ▼
50 logits
```

Conceptually:

```text
"a" → 0.02
"b" → 0.01
"c" → 0.03
...
" " → 0.21
...
```

These are converted into probabilities using softmax during generation.

---

## 📉 How Does the Model Learn?

The model needs to know when its prediction is wrong.

KindaGPT uses **cross-entropy loss**:

```python
loss = F.cross_entropy(logits, targets)
```

Conceptually:

$$
L = -\sum_i y_i \log(\hat{y}_i)
$$

If the correct next character is:

```text
"e"
```

and the model gives `"e"` a high probability, the loss is low.

If it gives `"e"` a tiny probability, the loss is high.

The training loop then uses backpropagation:

```python
optimizer.zero_grad(set_to_none=True)

loss.backward()

optimizer.step()
```

So the entire learning process becomes:

```text
Predict
   ↓
Compare with correct answer
   ↓
Calculate Loss
   ↓
Backpropagate
   ↓
Update Parameters
   ↓
Predict Again
```

---

## 🔄 The Complete KindaGPT Pipeline

At this point, we can put everything together.

```text
                     Raw Text
                        │
                        ▼
                 Character Tokens
                        │
                        ▼
                 Token Embeddings
                        │
                        +
                        │
               Position Embeddings
                        │
                        ▼
              ┌───────────────────┐
              │ Transformer Block │
              │                   │
              │  Self-Attention   │
              │       ↓           │
              │  Feed Forward     │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Transformer Block │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Transformer Block │
              └─────────┬─────────┘
                        │
                        ▼
                  LayerNorm
                        │
                        ▼
                  Linear Layer
                        │
                        ▼
                    Logits
                        │
                        ▼
                     Softmax
                        │
                        ▼
                Next Character
```

This is a tiny language model.

But conceptually, we're looking at the same family of architecture that eventually scales into modern GPT-style systems.

---

## ✍️ How Generation Actually Works

Training and generation are slightly different.

During training, we have the correct sequence available.

During generation, we don't.

The model has to generate one token at a time.

Suppose we start with:

```text
"H"
```

The model predicts:

```text
"e"
```

Now we have:

```text
"He"
```

The model predicts again:

```text
"l"
```

Now:

```text
"Hel"
```

and so on.

KindaGPT implements this autoregressive loop in `generate()`.

```text
Context
   │
   ▼
Predict next character
   │
   ▼
Convert logits → probabilities
   │
   ▼
Sample character
   │
   ▼
Append character to context
   │
   ▼
Repeat
```

The implementation samples from the probability distribution using:

```python
idx_next = torch.multinomial(
    probs,
    num_samples=1
)
```

rather than simply taking the character with the largest probability.

This introduces some variation into generation.

---

## 🔬 What I Actually Built

The final KindaGPT model is intentionally tiny:

| Component           | Configuration |
| ------------------- | ------------: |
| Token type          |     Character |
| Embedding size      |            32 |
| Context length      |             8 |
| Attention heads     |             4 |
| Transformer blocks  |             3 |
| Feed-forward size   |           128 |
| Batch size          |            32 |
| Learning rate       |         0.001 |
| Training iterations |         6,000 |
| Optimizer           |         AdamW |
| Loss                | Cross-Entropy |

The model also automatically uses CUDA when available:

```python
device = 'cuda' if torch.cuda.is_available() else 'cpu'
```

These numbers aren't intended to produce a powerful language model.

They're intentionally small enough that the architecture remains understandable. 

---

## 🧠 The Most Important Thing I Learned

The biggest takeaway from this project wasn't actually the code.

It was realizing that a Transformer isn't one magical component.

It is a collection of relatively understandable ideas working together:

```text
Tokenization
     ↓
Embeddings
     ↓
Position
     ↓
Attention
     ↓
Multi-Head Attention
     ↓
Feed Forward
     ↓
Residual Connections
     ↓
Layer Normalization
     ↓
Repeated Blocks
     ↓
Next-Token Prediction
```

Each piece has a relatively clear responsibility.

And when they are stacked together, something much more interesting emerges.

---

## 🤯 From "Attention" to GPT

There is an important distinction worth making.

**KindaGPT is not the original Transformer from the paper.**

The Transformer proposed in *Attention Is All You Need* is an **encoder-decoder architecture**, originally designed and evaluated for sequence-to-sequence tasks such as machine translation. ([arXiv][1])

KindaGPT is closer to the **decoder-only, autoregressive style** used by GPT-like language models.

Instead of:

```text
Encoder → Decoder → Output
```

we essentially have:

```text
Previous Tokens
      ↓
Masked Self-Attention
      ↓
Transformer Blocks
      ↓
Next Token
```

This distinction helped me understand something important:

> The Transformer is an architecture. GPT is one family of models built using Transformer ideas.

---

## 🧩 Why Build This Instead of Using Hugging Face?

A perfectly reasonable question is:

> "Why spend time implementing this when libraries already provide Transformers?"

Because the goal was different.

If I simply use:

```python
AutoModelForCausalLM.from_pretrained(...)
```

I can build something useful very quickly.

But I don't necessarily understand what happens inside it.

With KindaGPT, I had to explicitly implement:

```text
Q K V
      ↓
Attention
      ↓
Masking
      ↓
Softmax
      ↓
Multi-Head Attention
      ↓
Residual Connections
      ↓
Feed Forward
```

That forced me to confront the mathematics and tensor dimensions rather than treating the model as a black box.

The project was therefore less about building a useful LLM and more about **building intuition**.

---

## 🛠️ What Was Difficult?

### 1. Tensor Shapes

Attention involves several matrix multiplications, and understanding the dimensions was one of the more challenging parts.

For example:

```text
Input
(B, T, C)

Q
(B, T, head_size)

K
(B, T, head_size)

QKᵀ
(B, T, T)
```

That final dimension:

```text
(T, T)
```

represents every token comparing itself with every other token.

Once I understood that, attention became much less mysterious.

---

### 2. Causal Masking

The masking initially looked like a small implementation detail:

```python
masked_fill(...)
```

But conceptually it is extremely important.

Without it, the model could cheat during training by looking at future tokens.

The triangular matrix makes the autoregressive constraint explicit.

---

### 3. Understanding Q, K and V

The names themselves don't make the concept obvious.

It took some thinking to move from:

```text
Query
Key
Value
```

as abstract mathematical terms to:

```text
What am I looking for?
What information matches me?
What information should I retrieve?
```

That mental model made the attention mechanism much easier to understand.

---

## 🔮 Where I Want to Take This

KindaGPT is intentionally tiny, which makes it a good starting point for experimentation.

Some obvious next steps would be:

### Larger Context

The current context length is only:

```text
8 tokens
```

Increasing it would allow the model to use longer-range information.

### Better Tokenization

Character-level tokenization is great for learning but inefficient.

A natural next step would be implementing something like **Byte Pair Encoding (BPE)**.

### Better Generation

I would also like to experiment with:

* Temperature
* Top-k sampling
* Top-p sampling
* Different sampling strategies

### Larger Models

Increasing:

```text
Embedding dimension
Number of heads
Number of Transformer blocks
Context length
```

would allow experimentation with how model capacity affects learning.

### Visualizing Attention

One particularly interesting extension would be to visualize the attention matrices.

Instead of thinking about:

```text
QKᵀ
```

as a matrix of numbers, I could actually see:

```text
        The cat sat on the mat
The     █   ░   ░   ░   ░   ░
cat     █   █   ░   ░   ░   ░
sat     ░   █   █   ░   ░   ░
on      ░   ░   █   █   ░   ░
...
```

That would make the relationship between the mathematics and the model's behaviour much more tangible.

---

## 💭 Why This Project Matters to Me

I've been increasingly interested in understanding AI systems at a level deeper than simply knowing how to use them.

KindaGPT was one of those projects where the easiest approach would have been to use an existing implementation.

Instead, I wanted to take a step backwards and ask:

> **What would it take to actually build one?**

The resulting model is tiny and nowhere near the scale of modern LLMs.

But that wasn't really the point.

The important part was going from:

```text
"Transformers use attention."
```

to actually implementing:

```text
Q, K, V
↓
Scaled Dot-Product Attention
↓
Causal Mask
↓
Multi-Head Attention
↓
Feed Forward
↓
Residual Connections
↓
LayerNorm
↓
Next-Token Prediction
```

That transition—from knowing the terminology to understanding the mechanism—is what I wanted from this project.

---

## 🧩 Final Thoughts

The title **"Attention Is All You Need"** initially sounds almost too bold.

But after implementing even a tiny version of the architecture, the idea becomes much clearer.

The Transformer isn't magic.

At its core, it repeatedly performs a simple cycle:

```text
Look at the context
        ↓
Determine what matters
        ↓
Mix relevant information
        ↓
Transform that information
        ↓
Predict what comes next
```

KindaGPT is my attempt to make that process concrete.

It doesn't compete with a modern LLM.

It wasn't supposed to.

The goal was to take something that is often presented as a massive, complicated system and reduce it to a collection of components that I could understand, implement, and experiment with myself.

And for me, that's the real value of building models from scratch:

> **Sometimes the best way to understand an intelligent system is to build a deliberately small version of it yourself.**

---

### 📚 References

1. Vaswani, A. et al. **"Attention Is All You Need."** NeurIPS 2017. ([arXiv][1])


[1]: https://arxiv.org/abs/1706.03762 "Attention Is All You Need"