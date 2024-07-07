import os
import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Command failed with error: {stderr.decode()}")

def create_bootloader():
    with open('bootloader.asm', 'w') as f:
        f.write('''[BITS 32]
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
''')

    run_command('nasm -f bin -o bootloader.bin bootloader.asm')

def create_kernel():
    with open('kernel.c', 'w') as f:
        f.write('''void kernel_main() {
    const char *str = "Hello, Kernel World!";
    char *vidptr = (char*)0xb8000;  // video memory begins here
    unsigned int i = 0;
    unsigned int j = 0;

    // Clear screen
    while (j < 80 * 25 * 2) {
        vidptr[j] = ' ';
        vidptr[j+1] = 0x07;
        j = j + 2;
    }

    j = 0;

    // Display string
    while (str[j] != '\0') {
        vidptr[i] = str[j];
        vidptr[i+1] = 0x07;
        ++j;
        i = i + 2;
    }
}

void _start() {
    kernel_main();
    while (1) {
        __asm__ __volatile__("hlt");
    }
}
''')

    run_command('gcc -ffreestanding -m32 -c kernel.c -o kernel.o -fno-pie')
    run_command('ld -m elf_i386 -o kernel.bin -Ttext 0x1000 --entry=_start --oformat binary kernel.o')

def create_iso():
    os.makedirs('isodir/boot/grub', exist_ok=True)

    with open('grub.cfg', 'w') as f:
        f.write('''set timeout=0
set default=0

menuentry "myos" {
    multiboot /boot/kernel.bin
}
''')
    
    run_command('cp kernel.bin isodir/boot/')
    run_command('cp grub.cfg isodir/boot/grub/')
    run_command('grub-mkrescue -o myos.iso isodir')

def run_qemu():
    run_command('qemu-system-i386 -cdrom myos.iso -nographic')

if __name__ == "__main__":
    create_bootloader()
    create_kernel()
    create_iso()
    run_qemu()
