# Improving Large Language Models on One-hop Math Problems with Operation Embeddings

This repository contains the official source code for the paper **"Improving Large Language Models on One-hop Math Problems with Operation Embeddings"**.

## Setup

### Requirements
- **Hardware**: 2 GPUs with 24GB memory each (e.g., NVIDIA RTX 3090/A100)
- **LLaMA Checkpoints**: Obtain LLaMA-13B model weights and tokenizer from [Meta AI](https://github.com/facebookresearch/llama). Follow the official repository for access instructions.

### Training
- CUDA_VISIBLE_DEVICES=0,1 python -m torch.distributed.run \
--nproc_per_node 2 \
--master_port 1200 \
train_llama.py \
--ckpt_dir llama-2-13b \
--tokenizer_path llama-2-13b/tokenizer.model \
--input_file data/funcqa/curbest_same.json \
--lr 1e-4 \
--num_epochs 10 \
--dataset funcqa

  
### Inference
- CUDA_VISIBLE_DEVICES=0,1 python -m torch.distributed.run \
--nproc_per_node 2 \
--master_port 1250 \
inference_llama.py \
--ckpt_dir llama-2-13b \
--tokenizer_path llama-2-13b/tokenizer.model \
--mode func_embedding \
--dataset funcqa_oh \
--func_load_path checkpoints/funcqa/epoch_5.pth \
--logits_bias 4.4

## Acknowledgement
This work builds upon [ToolkenGPT](https://github.com/Ber666/ToolkenGPT). We sincerely thank the authors for their foundational contributions to tool-augmented language modeling.
