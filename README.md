# Tugas-Besar-III-IF2211-Strategi-Algoritma
Penerapan String Matching dan Regular Expression dalam Pembangunan Deadline Reminder Assistant

## General info
Tugas Besar kali ini merupakan tugas yang mengharuskan kami untuk mengimplementasikan algoritma pattern matching (string matching) untuk melakukan pengenalan pola-pola tertentu pada masukan yang diberikan oleh user. Pola-pola tersebut utamanya adalah berupa kalimat-kalimat “penting” yang mendefinisikan suatu perintah yang valid yang dapat dimasukan user ke dalam query chatbot.

Dengan menggunakan algoritma pencocokan string, kami berusaha untuk menemukan ada kata penting apa saja yang terkandung di dalam query yang diberikan oleh user. Secara garis besar, kami mengimplementasikan algoritma pencocokan string Boyer-Moore (BM) dan algoritma Knuth-Morris-Pratt (KMP). Dengan beberapa pertimbangan, utamanya mempertimbangkan dari efisiensi eksekusi algoritma untuk menangani kasus yang ada, kami memilih algoritma BM sebagai algoritma utama untuk melakukan pencocokan string.

Selain menggunakan algoritma BM, kami juga menggunakan Regular Expression (regex) untuk membantu menemukan pola pola yang lebih general dalam masukan yang diberikan oleh user. Regex utamanya kami gunakan dalam menentukan input yang berupa pola-pola tertentu, namun masukannya bisa sangat berbeda dari satu masukan ke masukan lain.


## Requirements
Python 3.8\
pip install flask\
pip install flask_sqlalchemy

## Author
Disusun Oleh:\
Jose Galbraith Hasintongan	13519022\
Febriawan Ghally Ar Rahman 	13519111\
Muhammad Akram Al Bari		13519142
