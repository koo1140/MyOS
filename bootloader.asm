[BITS 32]
[ORG 0x100000]

; Multiboot header
%define MULTIBOOT_HEADER_MAGIC 0x1BADB002
%define MULTIBOOT_HEADER_FLAGS 0x0
%define CHECKSUM -(MULTIBOOT_HEADER_MAGIC + MULTIBOOT_HEADER_FLAGS)

section .multiboot
    align 4
    dd MULTIBOOT_HEADER_MAGIC
    dd MULTIBOOT_HEADER_FLAGS
    dd CHECKSUM

section .text
    global start
    extern kernel_main

start:
    ; Your bootloader code here
    ; Example: Load kernel, setup environment, etc.

    ; Jump to kernel
    mov eax, MULTIBOOT_HEADER_MAGIC
    mov ebx, 0
    call kernel_main
    cli
    hlt
