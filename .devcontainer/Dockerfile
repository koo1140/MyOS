FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu

# Install required packages
RUN apt-get update && apt-get install -y \
    qemu-system-x86 \
    gcc \
    nasm \
    grub-pc-bin \
    xorriso \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
