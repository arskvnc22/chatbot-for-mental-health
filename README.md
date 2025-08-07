# ThriveBot: An Experimental ADHD Chatbot Using Hybrid RAG and LoRA Architecture

ThriveBot is an experimental, prototype conversational agent designed to provide informational support for individuals interested in Attention-Deficit/Hyperactivity Disorder (ADHD). This project explores a novel hybrid architecture that combines Retrieval-Augmented Generation (RAG) for factual accuracy with multiple Low-Rank Adaptation (LoRA) modules to offer distinct conversational styles.

> ⚠️ **Disclaimer:**  
> This is a research prototype and is not a medical device or a substitute for professional medical advice, diagnosis, or treatment. It was developed for academic purposes to explore AI techniques in a controlled environment.

---

## 🌟 Features

- **Hybrid AI Architecture**  
  Integrates a RAG system to ground responses in a curated knowledge base with LoRA adapters for stylistic flexibility.

- **Dynamic Conversational Styles**  
  Users can switch between different personas on-the-fly:
  - **Therapist-like**: Offers warm, validating, and emotionally supportive responses.
  - **Casual**: Provides a friendly, peer-like, and informal conversational experience.
  - **Balanced**: A middle-ground style blending informative and supportive interaction.

- **Factual & Relevant Information**  
  The RAG system pulls from a specialized knowledge base created from expert content (e.g., Dr. Andrew Huberman's discussions on ADHD) to answer questions accurately.

- **Safety-Conscious Design**  
  Built on Llama 3.1, which includes safety mitigations, and developed with ethical considerations at the forefront.

- **Interactive Web Interface**  
  A user-friendly chat interface built with Gradio allows for easy interaction and style selection.

---

## 🧠 Retrieval-Augmented Fine-Tuning (RAFT)

The fine-tuning process was designed not only to teach the model different conversational styles but also to train it on how to interact with the RAG system effectively.

### Integrating RAG Context into Fine-Tuning

To make the model aware of the RAG system, the retrieved factual context was directly integrated into the training data.

- **Structured Prompts**  
  Each example in the Supervised Fine-Tuning (SFT) dataset was formatted to include a dedicated section for retrieved information. The training prompt explicitly presented this to the model, for example:


Facts: 
[Retrieved context snippet 1]
[Retrieved context snippet 2]


- **Learning from Examples**  
By including this `Facts:` block in every training sample (even when empty), the model learned to recognize and expect this contextual information as part of its input, conditioning it to ground its responses when facts are available.

---

### Teaching the Model to Discern Context

A key challenge is teaching the model not to blindly use any information it's given. It must learn to differentiate between relevant and irrelevant context.

- **Mixed-Relevance Training Data**  
The SFT dataset was intentionally populated with a mix of examples:
- **Relevant Context**: The response incorporated relevant facts naturally.
- **Irrelevant Context**: The response ignored unrelated facts and focused on the user's situation.

- **Training for Abstention**  
To prevent hallucination, the dataset included cases where the model should admit it doesn't know (e.g., _"I don't have enough information to answer that."_).  
However, GPT-4o-mini failed to follow this instruction in the data generation process, so this was a failure.

- **Developing Discernment**  
By training on thousands of these mixed examples, the model learned to assess context relevance, avoiding fact parroting.

---

## 🛠️ Tech Stack & Architecture

ThriveBot is built with a combination of cutting-edge open-source technologies.

### Core Components

- **Base Model**: Meta Llama 3.1 8B Instruct
- **Fine-Tuning**: Parameter-Efficient Fine-Tuning (PEFT) with LoRA

### Knowledge Retrieval (RAG)

- **Embedding Model**: `sentence-transformers/multi-qa-MiniLM-L6-cos-v1`
- **Vector Database**: FAISS (Facebook AI Similarity Search)

### Frameworks & Libraries

- PyTorch  
- Hugging Face: `transformers`, `datasets`, `peft`  
- Unsloth for optimized LoRA training  
- Gradio for the web interface

---

### Architecture Overview

1. **User Input**  
 Sent via Gradio UI with style selection

2. **Style Switching**  
 Detects style change, activates LoRA adapter, recalculates KV cache

3. **RAG Retrieval**  
 Embeds query and retrieves documents from FAISS

4. **Prompt Formatting**  
 Includes system message, context, history, and user input

5. **Response Generation**  
 Model generates response using selected LoRA style

6. **Safety Check**  
 Output is reviewed before display

---

## 📊 Dataset Curation & Generation

Performance hinges on high-quality training data. A mix of curated expert content and synthetic data was used.

### RAG Knowledge Base (Factual Grounding)

- **Source**: Dr. Andrew Huberman's talk, _"ADHD & How Anyone Can Improve Their Focus"_
- **Process**: Converted to 532 question-answer pairs
- **Content**: Covers symptoms, supplements, sleep, etc.

---

### SFT Datasets for Stylistic LoRA Adapters

To teach distinct styles, synthetic datasets were created.

- **Base Scenarios**: Empathetic Dialogues dataset
- **Generation Engine**: GPT-4o-mini
- **Pipeline**:
- Metadata tagging: emotional depth, situation type, RAG relevance
- Few-shot prompting: guides GPT-4o-mini

- **Result**:  
1,100+ styled examples per persona, with RAG context

> _Diagram of the data generation pipeline:_  
> _(<img width="777" height="326" alt="image" src="https://github.com/user-attachments/assets/c0f5225d-a09e-4742-91c1-084f3a97874c" />
)_

---

### Real-World Therapeutic Data

Used for enhanced nuance in "therapist-like" style.

- **Source**: Counsel Chat dataset
- **Trade-offs**:
- Richer language
- Introduced artifacts and safety concerns
- Demonstrated the tension between safety and stylistic realism
- Demonstrated the difference between training on synthetic and real world data
---

## 🚀 Getting Started

To run ThriveBot:

### Prerequisites

- Python 3.11+  
- PyTorch with CUDA support  
- Hugging Face account

### Installation

```bash
git clone https://github.com/arskvnc22/chatbot-for-mental-health.git
cd chatbot-for-mental-health
pip install -r requirements.txt
```

3. Environment Setup
Ensure your Hugging Face token is available as an environment variable to download the gated Llama 3.1 model.

export HUGGING_FACE_HUB_TOKEN='your_hf_token_here'

4. Running the Application
Launch the Gradio web interface with the following command:


### ⚖️ Ethical Considerations
Developing an AI for mental health support carries significant ethical responsibilities. This project was guided by the following principles:

User Safety: The system is designed to avoid providing medical diagnoses, handling crisis situations, or generating harmful content. Clear disclaimers are provided.

Privacy: ThriveBot does not require user accounts or store conversation data, ensuring user anonymity.

Data Scarcity & Bias: The project acknowledges the limitations of available data. The "therapist-like" style, when trained on real-world data like the Counsel Chat dataset, inherited biases and safety issues, highlighting the critical need for expert-curated datasets.

Transparency: This README and the accompanying report aim to be fully transparent about the model's capabilities, limitations, and the trade-offs discovered during research.

### 🔮 Future Work
This project lays the groundwork for several exciting future directions:

Improved Datasets: The most critical next step is the creation of high-quality, ethically sourced, and expert-validated datasets for fine-tuning therapeutic conversational styles.

Advanced RAG: Implementing more advanced RAG techniques, such as cross-encoder rerankers and fine-tuning the embedding model itself.

Enhanced Safety Protocols: Integrating more robust mechanisms for detecting user distress and providing appropriate signposting to professional help.

Long-Term Memory: Exploring methods for the chatbot to have a longer, more coherent memory of the conversation.

### 🙏 Acknowledgements
This project was submitted for the BSc in Computer Science at the University of Hull.

The RAG knowledge base was curated from content by Dr. Andrew Huberman.

The LoRA adapters were trained using synthetic datan from the Empathetic Dialogues dataset and the real data from the Counsel Chat dataset.

- Special thanks to the consulting psychiatrist for their invaluable feedback and professional evaluation of the model's responses.
