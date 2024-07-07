[BITS 32]
[ORG 0x7c00]

start:
  mov ax, 0x07C0
  mov ds, ax

  mov si, msg
  call print_string

  jmp $ 

print_string:
  mov ah, 0x0E
.loop:
  lodsb       
  cmp al, 0    
  je .done
  int 0x10    
  jmp .loop
.done:
  ret

msg:
  db 'Hello from ZapOS (bootloader)!', 13, 10, 0 

times 510-($-$$) db 0 
dw 0xAA55    