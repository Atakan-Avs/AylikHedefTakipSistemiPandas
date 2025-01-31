import pandas as pd
import numpy as np
from datetime import datetime, timedelta

#subat ayi icin gun olusturma
baslangic_tarih = datetime(2025, 2, 1)
bitis_tarih = datetime(2025, 2, 28)
gunler = [(baslangic_tarih + timedelta(days=i)).strftime('%d-%m-%Y') for i in range((bitis_tarih - baslangic_tarih).days + 1)]

#DataFrame olustur
df = pd.DataFrame({
    'Gün': gunler,
    'Stratejik_Fokus1': 0,
    'Cihaz_Yna_Ciro': 0,
    'yt_post': 0,
    'mnp_post': 0,
    'yt_pre': 0,
    'Pre_to_post': 0,
    'mccm': 0,
    'Vfnet': 0
})

#hedefleri gir
hedefler = {
    'Stratejik_Fokus1': 250,
    'Cihaz_Yna_Ciro': 0,
    'yt_post': 0,
    'mnp_post': 0,
    'yt_pre': 0,
    'Pre_to_post': 0,
    'mccm': 0,
    'Vfnet': 0
}

#gunluk hedefleri hesapla
df['günlük_hedef_stratejik_fokus1'] = hedefler['Stratejik_Fokus1'] / len(gunler)
df['günlük_hedef_cihaz_yna_ciro'] = hedefler['Cihaz_Yna_Ciro'] / len(gunler)
df['günlük_hedef_yt_post'] = hedefler['yt_post'] / len(gunler)
df['günlük_hedef_mnp_post'] = hedefler['mnp_post'] / len(gunler)
df['günlük_hedef_yt_pre'] = hedefler['yt_pre'] / len(gunler)
df['günlük_hedef_pre_to_post'] = hedefler['Pre_to_post'] / len(gunler)
df['günlük_hedef_mccm'] = hedefler['mccm'] / len(gunler)
df['günlük_hedef_vfnet'] = hedefler['Vfnet'] / len(gunler)

#dataframi csv ye kaydet
df.to_csv('hedefler.csv', index=False)
print("Başlangic dosyasi 'hedefler.csv' olarak kaydedildi")

def guncelle_ve_analiz_et(dosyaAdi, gun, yeniVeriler):
    """
    Parametreler:
    dosya_adi: Hedeflerin saklandigi CSV dosyasinin adi
    gun: Günlük gerçekleşmenin girileceği gün (format: 'dd-mm-yyyy')
    yeni_veriler: Günlük gerçekleşmeleri içeren bir sözlük
    """
    #dosya oku ve dataframe ekle
    df = pd.read_csv(dosyaAdi)

    #günü bul ve yeni gerceklesen degeri gir
    gun_tarihi = datetime.strptime(gun, '%d-%m-%Y').strftime('%d-%m-%Y')
    for hedef, deger in yeniVeriler.items():
        df.loc[df['Gün'] == gun_tarihi, hedef] = deger

    #hedeflere ulasma yuzdesi
    for hedef in hedefler.keys():
        toplam = df[hedef].sum()
        yuzde = (toplam / hedefler[hedef]) * 100 if hedefler[hedef] > 0 else 0
        print(f"{hedef} için toplam gerçekleşme: {toplam}, Hedefe ulaşma yüzdesi: {yuzde:.2f}%")

    #gunluk yapilmasi gereken yeni degerler
    kalan_gunler = len(df[df['Gün'] >= gun_tarihi])
    for hedef in hedefler.keys():
        kalan = max(0, hedefler[hedef] - df[hedef].sum())
        print(f"{hedef} için günlük yapilmasi gereken yeni değer: {kalan / max(1, kalan_gunler):.2f}")

    #guncellenmis dataframe i tekrardan kaydet
    df.to_csv(dosyaAdi, index=False)
    print(f"'{dosyaAdi}' dosyasi güncellendi")

#1 subat gunu gerceklesen adetler ( ornek olarak )
gunluk_veriler = {
    'Stratejik_Fokus1': 100,
    'Cihaz_Yna_Ciro': 2000,
    'yt_post': 2,
    'mnp_post': 1,
    'yt_pre': 3,
    'Pre_to_post': 1,
    'mccm': 0,
    'Vfnet': 2
}

guncelle_ve_analiz_et('hedefler.csv', '01-02-2025', gunluk_veriler)

