ThriveBot: An Experimental ADHD ChatbotUsing Hybrid RAG and LoRA Architecture

ThriveBot is an experimental, prototype conversational agent designed to provide informational support for individuals interested in Attention-Deficit/Hyperactivity Disorder (ADHD). This project explores a novel hybrid architecture that combines Retrieval-Augmented Generation (RAG) for factual accuracy with multiple Low-Rank Adaptation (LoRA) modules to offer distinct conversational styles.

Disclaimer: 🛑 This is a research prototype and is not a medical device or a substitute for professional medical advice, diagnosis, or treatment. It was developed for academic purposes to explore AI techniques in a controlled environment.

🌟 Features
Hybrid AI Architecture: Integrates a RAG system to ground responses in a curated knowledge base with LoRA adapters for stylistic flexibility.

Dynamic Conversational Styles: Users can switch between different personas on-the-fly:

Therapist-like: Offers warm, validating, and emotionally supportive responses.

Casual: Provides a friendly, peer-like, and informal conversational experience.

Balanced: A middle-ground style blending informative and supportive interaction.

Factual & Relevant Information: The RAG system pulls from a specialized knowledge base created from expert content (e.g., Dr. Andrew Huberman's discussions on ADHD) to answer questions accurately.

Safety-Conscious Design: Built on Llama 3.1, which includes safety mitigations, and developed with ethical considerations at the forefront.

Interactive Web Interface: A user-friendly chat interface built with Gradio allows for easy interaction and style selection.
🧠 Retrieval-Augmented Fine-Tuning (RAFT)
The fine-tuning process was designed not only to teach the model different conversational styles but also to train it on how to interact with the RAG system effectively.

Integrating RAG Context into Fine-Tuning
To make the model aware of the RAG system, the retrieved factual context was directly integrated into the training data.

Structured Prompts: Each example in the Supervised Fine-Tuning (SFT) dataset was formatted to include a dedicated section for retrieved information. The training prompt explicitly presented this to the model, for example:

Facts: 
[Retrieved context snippet 1]
[Retrieved context snippet 2]

Learning from Examples: By including this Facts: block in every training sample (even when empty), the model learned to recognize and expect this contextual information as part of its input, conditioning it to ground its responses when facts are available.

Teaching the Model to Discern Context
A key challenge is teaching the model not to blindly use any information it's given. It must learn to differentiate between relevant and irrelevant context.

Mixed-Relevance Training Data: The SFT dataset was intentionally populated with a mix of examples:

Relevant Context: Scenarios where the retrieved facts were directly relevant to the user's situation. In these cases, the target response was written to correctly and naturally incorporate the information.

Irrelevant Context: Scenarios where the retrieved facts were unrelated to the user's query. Here, the target response was written to completely ignore the irrelevant facts and focus solely on the user's emotional or situational needs.

Training for Abstention (Handling "I Don't Know"): A crucial aspect of preventing factual hallucination is teaching the model to abstain from answering when the retrieved context is insufficient. The SFT dataset included examples where the correct response was an admission of not knowing (e.g., "I don't have enough information to answer that"). This is a difficult behavior to instill consistently, as models are often prone to generating an answer regardless, but it is a critical step toward building a more reliable and trustworthy AI. However GPT 4o mini failed to follow this instruction in the data generation process so this wasa failure.

Developing Discernment: By training on thousands of these mixed examples, the model learned to assess the relevance of the provided context. This prevents the model from simply "parroting" facts and encourages it to generate responses that are both factually accurate and contextually appropriate.
🛠️ Tech Stack & Architecture
ThriveBot is built with a combination of cutting-edge open-source technologies.

Core Components:
Base Model: Meta Llama 3.1 8B Instruct serves as the foundational large language model.

Fine-Tuning: Parameter-Efficient Fine-Tuning (PEFT) with LoRA is used to train the stylistic adapters efficiently.

Knowledge Retrieval (RAG):

Embedding Model: sentence-transformers/multi-qa-MiniLM-L6-cos-v1 for creating semantic vector representations.

Vector Database: FAISS (Facebook AI Similarity Search) for efficient similarity search.

Frameworks & Libraries:

PyTorch

Hugging Face transformers, datasets, and peft

Unsloth for optimized LoRA training.

Gradio for the web interface.

Architecture Overview:
The system's logic is designed to be style-aware, contextually grounded, and mindful of resource limitations.

User Input: The user sends a message and selects a conversational style via the Gradio UI.

Style Switching: The system detects if the style has been changed. If so, it activates the corresponding LoRA adapter and recalculates the KV cache to ensure stylistic consistency.

RAG Retrieval: The user's query is embedded and used to search the FAISS vector index for relevant documents from the ADHD knowledge base.

Prompt Formatting: A final prompt is constructed, including a system message, the retrieved RAG context, conversation history, and the user's input, all formatted for Llama 3.1.

Response Generation: The model generates a response based on the assembled prompt and the active LoRA adapter's style.

Safety Check: The response is reviewed for safety before being displayed to the user.

📊 Dataset Curation & Generation
The performance of ThriveBot is fundamentally tied to the quality of its training data. Given the scarcity of high-quality, ethically-sourced data in the mental health domain, this project employed a multi-faceted approach to dataset creation, combining curated expert content with programmatically generated synthetic data.

1. RAG Knowledge Base (Factual Grounding)
To ensure factual accuracy, the RAG system is grounded in a specialized knowledge base.

Source: The primary source is a detailed transcript of Dr. Andrew Huberman's YouTube discussion, "ADHD & How Anyone Can Improve Their Focus."

Process: The transcript was converted into a series of question-answer pairs, creating a focused and reliable set of documents for retrieval.

Content: This knowledge base contains 532 distinct QA pairs covering ADHD symptoms, characteristics, supplements, sleep schedules, and related topics.

2. SFT Datasets for Stylistic LoRA Adapters
To teach the model its distinct "casual" and "therapist-like" personas, synthetic datasets were generated using a custom pipeline.

Base Scenarios: Real-life situations were sourced from the Empathetic Dialogues dataset.

Generation Engine: GPT-4o-mini was used to generate styled responses for these situations.

Generation Pipeline: A rule-based, two-step approach was used:

Metadata Tagging: Each situation was programmatically analyzed and tagged for emotional depth, situation type, and relevance of the retreived RAG context.

Few-Shot Prompting: Based on the tags, a highly specific prompt with few-shot examples was constructed to guide GPT-4o-mini in generating a response that matched the desired style.

Result: This process yielded over 1,100 unique, styled examples for each persona, complete with RAG context where appropriate.

Diagram of the data generation pipeline:
(Your diagram can be placed here)

3. Real-World Therapeutic Data
While synthetic data proved effective for the "casual" style, it lacked the nuance required for a convincing "therapist-like" persona.

Source: To introduce more conversational variance, an adapter was also trained on the publicly available Counsel Chat dataset.

Trade-offs: This dataset provided richer, more varied therapeutic language but also introduced significant challenges, including safety risks, diagnostic language, and other artifacts that required careful management. This highlights the critical trade-off between the safety of synthetic data and the variance of real-world data.

🚀 Getting Started
To run ThriveBot locally, you will need a Python environment and a machine with a capable GPU (e.g., NVIDIA L4, A100).

1. Prerequisites
Python 3.11+

PyTorch with CUDA support

Access to a Hugging Face account

2. Installation
Clone the repository and install the required dependencies:

git clone https://github.com/your-username/ThriveBot.git
cd ThriveBot
pip install -r requirements.txt

3. Environment Setup
Ensure your Hugging Face token is available as an environment variable to download the gated Llama 3.1 model.

export HUGGING_FACE_HUB_TOKEN='your_hf_token_here'

4. Running the Application
Launch the Gradio web interface with the following command:

python app.py

Navigate to the local URL provided by Gradio (e.g., http://127.0.0.1:7860) in your web browser to start chatting with ThriveBot.

⚖️ Ethical Considerations
Developing an AI for mental health support carries significant ethical responsibilities. This project was guided by the following principles:

User Safety: The system is designed to avoid providing medical diagnoses, handling crisis situations, or generating harmful content. Clear disclaimers are provided.

Privacy: ThriveBot does not require user accounts or store conversation data, ensuring user anonymity.

Data Scarcity & Bias: The project acknowledges the limitations of available data. The "therapist-like" style, when trained on real-world data like the Counsel Chat dataset, inherited biases and safety issues, highlighting the critical need for expert-curated datasets.

Transparency: This README and the accompanying report aim to be fully transparent about the model's capabilities, limitations, and the trade-offs discovered during research.

🔮 Future Work
This project lays the groundwork for several exciting future directions:

Improved Datasets: The most critical next step is the creation of high-quality, ethically sourced, and expert-validated datasets for fine-tuning therapeutic conversational styles.

Advanced RAG: Implementing more advanced RAG techniques, such as cross-encoder rerankers and fine-tuning the embedding model itself.

Enhanced Safety Protocols: Integrating more robust mechanisms for detecting user distress and providing appropriate signposting to professional help.

Long-Term Memory: Exploring methods for the chatbot to have a longer, more coherent memory of the conversation.

🙏 Acknowledgements
This project was submitted for the BSc in Computer Science at the University of Hull.

The RAG knowledge base was curated from content by Dr. Andrew Huberman.

The LoRA adapters were trained using the Empathetic Dialogues and Counsel Chat datasets.

Special thanks to the consulting psychiatrist for their invaluable feedback and professional evaluation of the model's responses.
