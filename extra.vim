inoremap <C-i> <C-i>
inoremap <C-m> <C-m>
cnoremap <C-m> <C-m>
nnoremap XX ZZ
vnoremap <nowait> i l
nnoremap <nowait> z b
vnoremap <nowait> z b
noremap <nowait> z b
noremap O :
noremap : P

augroup colemak_dh 
    au!
    au FileType qf nnoremap <buffer> <CR> <CR>
    au FileType help nmap <buffer> gY gO
augroup END
