void kernel_main() {
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
    while (str[j] != ' ') {
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
