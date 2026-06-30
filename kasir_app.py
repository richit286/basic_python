import json
from datetime import datetime 

FILE_MENU = "menu.json"
FILE_DATA = "riwayat_pembelian.json"

# Membaca menu dari file JSON
with open(FILE_MENU, 'r') as f:
    menu = json.load(f)

# Membuat dictionary untuk menyimpan harga dan nama menu
harga = {int(k): v['harga'] for k, v in menu.items()}
nama = {int(k): v['nama'] for k, v in menu.items()}

def minta_int_positif(pesan):
    while True:
        try:
            nilai = int(input(pesan))
            if nilai > 0:
                return nilai
            else:
                print("Masukkan harus berupa bilangan bulat positif.")
        except ValueError:
            print("Masukkan tidak valid. Silakan masukkan bilangan bulat positif.")

def muat_menu():
    print("\nMenu:")
    for k in sorted(menu.keys()):
        item = menu[k]
        print(f"{k}. {item['nama']} - Rp {item['harga']:,}")
    
    # Meminta input dari pengguna untuk memilih menu
    pilihan = minta_int_positif("Masukkan nomor menu yang ingin dibeli (1-3): ")
    if pilihan not in harga:
        print("Pilihan tidak valid. Silakan pilih menu yang tersedia.")
        return None, None

    # Meminta input dari pengguna untuk jumlah kg yang ingin dibeli
    jumlah = minta_int_positif(f"Masukkan jumlah kg {nama[pilihan]} yang ingin dibeli: ")
    return pilihan, jumlah

def hitung_total(pilihan, jumlah):
    total_diskon = 0
    # Menghitung total harga dengan diskon jika berlaku
    if pilihan == 1 and jumlah >= 5:
        total_harga = (harga[pilihan] * jumlah) * 0.9
        total_diskon = (harga[pilihan] * jumlah) * 0.1
        print(f"\nSelamat! Anda mendapatkan diskon 10%.")
    elif pilihan == 2 and jumlah >= 2:
        total_harga = (harga[pilihan] * jumlah) * 0.85
        total_diskon = (harga[pilihan] * jumlah) * 0.15
        print(f"\nSelamat! Anda mendapatkan diskon 15%.")
    elif pilihan == 3 and jumlah >= 3:
        total_harga = (harga[pilihan] * jumlah) * 0.88
        total_diskon = (harga[pilihan] * jumlah) * 0.12
        print(f"\nSelamat! Anda mendapatkan diskon 12%.")
    else:
        total_harga = harga[pilihan] * jumlah

    return total_harga, total_diskon

def struk_pembelian(antrian, riwayat, riwayat_diskon, grand_total):
    # Menampilkan struk pembelian
    print("\n======== STRUK PEMBELIAN ========")
    if riwayat_diskon:
        print("\n====== RIWAYAT DISKON ======")
        for t in riwayat_diskon:
            print(f"{t['jumlah']} kg {t['item']:<5} = Rp {t['potongan']:,.0f}")
    print("\n===== RIWAYAT PEMBELIAN =====")
    for t in riwayat:
        print(f"{t['jumlah']} kg {t['item']:<5} = Rp {t['subtotal']:,.0f}")
    print("---------------------------")
    print(f"TOTAL KESELURUHAN = Rp {grand_total:,.0f}")

def layani_pelanggan(antrian):
    riwayat = []
    riwayat_diskon = []
    grand_total = 0

    while True:
        pilihan, jumlah = muat_menu()
        if pilihan is None or jumlah is None:
            continue

        total_harga, total_diskon = hitung_total(pilihan, jumlah)
        if total_diskon > 0:
            riwayat_diskon.append({"item": nama[pilihan], "jumlah": jumlah, "potongan": total_diskon})

        # Menampilkan total harga yang harus dibayar
        print(f"\nTotal harga untuk {jumlah} kg {nama[pilihan]} adalah Rp {total_harga:,.0f}")

        # Menyimpan riwayat pembelian dan menambahkan ke total keseluruhan
        riwayat.append({"item": nama[pilihan], "jumlah": jumlah, "subtotal": total_harga})
        grand_total += total_harga

        beli_lagi = input("Apakah Anda ingin membeli lagi? (y/n): ")
        if beli_lagi.lower() != 'y':
            break

    struk_pembelian(antrian, riwayat, riwayat_diskon, grand_total)

    return {
        "antrian": antrian,
        "riwayat": riwayat,
        "riwayat_diskon": riwayat_diskon,
        "grand_total": grand_total
    }

                                                                        
def simpan_data(semua_transaksi, total_toko):
    # SAVE hasil sesi ini
    data = {
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "jumlah_pelanggan": len(semua_transaksi),
        "total_toko": total_toko,
        "transaksi": semua_transaksi
    }
    with open(FILE_DATA, "w") as f:
        json.dump(data, f, indent=4)

def jalankan_kasir():
    semua_transaksi = []
    total_toko = 0
    antrian = 1

    print("===== TOKO DAGING BUKA =====")
    while True:
        status = input(f"\n[Pelanggan #{antrian}] Tekan ENTER untuk mulai, ketik 'tutup' untuk tutup toko: ")
        if status.lower() == 'tutup':
            break
        
        transaksi = layani_pelanggan(antrian)
        semua_transaksi.append(transaksi)
        total_toko += transaksi["grand_total"]
        antrian += 1

    # Rekap Toko
    print("\n===== REKAP TOKO =====")
    print(f"Jumlah pelanggan hari ini: {len(semua_transaksi)}")
    print(f"Total pendapatan toko hari ini: Rp {total_toko:,.0f}")

    simpan_data(semua_transaksi, total_toko)
    print(f"\nData transaksi telah disimpan ke {FILE_DATA}.")

if __name__ == "__main__":
    jalankan_kasir()