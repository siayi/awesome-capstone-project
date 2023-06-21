# sortir.py

"""
    Pendekatan yang diambil dijelaskan di bawah ini.
    Saya memilih untuk melakukannya dengan cara yang sederhana. 
    Awalnya, saya mempertimbangkan untuk mem-parsing data
    ke dalam struktur tertentu dan kemudian menghasilkan file README yang sesuai.
    Saya masih mempertimbangkan untuk melakukannya,
    namun untuk saat ini seharusnya ini sudah berfungsi.
    Satu-satunya masalah yang saya lihat adalah bahwa pengurutan
    hanya dilakukan pada entri di tingkat terendah,
    dan urutan konten tingkat atas tidak sesuai dengan urutan entri yang sebenarnya.
    
    Ini bisa diperluas dengan memiliki blok-blok bersarang,
    mengurutkannya secara rekursif, dan menyatukan struktur akhir menjadi daftar baris.
    Mungkin ada revisi kedua.
"""

def sort_blocks():
    # Pertama, kita memuat README saat ini ke dalam memori
    with open('README.md', 'r') as read_me_file:
        read_me = read_me_file.read()

    # Memisahkan 'TOC' dari konten (blok-blok)
    TOC = ''.join(read_me.split('- - -')[0])
    blocks = ''.join(read_me.split('- - -')[1]).split('\n# ')

    # Memperbaiki format blok-blok
    for i in range(len(blocks)):
        if i == 0:
            blocks[i] = blocks[i] + '\n'
        else:
            blocks[i] = '# ' + blocks[i] + '\n'

    # Mengurutkan blok pertama
    inner_blocks = sorted(blocks[0].split('##'))
    for i in range(1, len(inner_blocks)):
        if inner_blocks[i][0] != '#':
            inner_blocks[i] = '##' + inner_blocks[i]
    inner_blocks = ''.join(inner_blocks)

    # Menggantikan blok-blok yang belum diurutkan dengan yang telah diurutkan dan menggabungkannya menjadi final_README
    blocks[0] = inner_blocks
    final_README = TOC + '- - -' + ''.join(blocks)
    
    # Menulis final_README ke file README.md
    with open('README.md', 'w+') as sorted_file:
        sorted_file.write(final_README)

def main():
    # Membaca README saat ini ke dalam memori sebagai array dari setiap baris
    with open('README.md', 'r') as read_me_file:
        read_me = read_me_file.readlines()

    # Then we cluster the lines together as blocks
    # Each block represents a collection of lines that should be sorted
    # This was done by assuming only links ([...](...)) are meant to be sorted
    # Mengelompokkan baris-baris menjadi blok-blok
    blocks = []
    last_indent = None
    for line in read_me:
        s_line = line.lstrip()
        indent = len(line) - len(s_line)

        # Mengelompokkan hanya baris yang merupakan tautan ([...](...)) dan mengabaikan baris lainnya
        if any([s_line.startswith(s) for s in ['* [', '- [']]):
            if indent == last_indent:
                blocks[-1].append(line)
            else:
                blocks.append([line])
            last_indent = indent
        else:
            blocks.append([line])
            last_indent = None

    # Menulis blok-blok yang telah diurutkan kembali ke file README.md
    with open('README.md', 'w+') as sorted_file:
        # Then all of the blocks are sorted individually
        blocks = [
            ''.join(sorted(block, key=str.lower)) for block in blocks
        ]
        # And the result is written back to README.md
        sorted_file.write(''.join(blocks))

    # Memanggil fungsi sort_blocks() untuk mengurutkan bagian-bagian tertentu dalam file README.md
    sort_blocks()


if __name__ == "__main__":
    main()
