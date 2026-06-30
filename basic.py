daging = 1000
harga_per_kg = 30000
total_harga = 0
daging_dibeli = 0

while daging>0:
    print("Jumlah daging:", daging, "kg")
    daging_dibeli += float(input("Masukkan jumlah daging yang ingin dibeli (kg): "))
    if daging_dibeli <= 0:
        print("Jumlah daging yang dibeli harus lebih dari 0 kg.")
    elif daging_dibeli > daging:
        print("Maaf, stok daging tidak cukup. Stok tersedia:", daging, "kg")
    else:
        if daging_dibeli >= 5:
            total_harga += (daging_dibeli * harga_per_kg)-7000
        elif daging_dibeli > 2:
            total_harga += (daging_dibeli * harga_per_kg)-5000
        else:
            total_harga += float(daging_dibeli * harga_per_kg)
        
        print(f"Total harga untuk {daging_dibeli} kg daging adalah Rp {total_harga:,.0f}")
        daging -= daging_dibeli

        beli_lagi = input("Apakah Anda ingin membeli lagi? (y/n): ")
        if beli_lagi.lower() != 'y':
            break

else:
    print("Stok daging habis.")
