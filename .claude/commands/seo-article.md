# SEO Uyumlu Blog Makalesi Yazma

Bu komut, Lektor CMS formatında SEO optimizasyonlu blog makalesi yazmak için kullanılır.

## Kullanıcıdan Alınacak Bilgiler

Başlamadan önce şunları sor:
1. **Konu:** Makale konusu / ana tez
2. **Dil:** Türkçe mi İngilizce mi (ikisi de mi?)
3. **Ana anahtar kelime:** Google'da hangi arama terimiyle bulunmalı?
4. **Slug:** URL slug (yoksa kendin öner)
5. **Notlar/kaynaklar:** Varsa ham notlar veya referans materyaller

## Makale Yapısı

Her makale şu sırayı izlemeli:

### 1. Giriş (3 paragraf, sade ve odaklı)
- **Paragraf 1:** Problemi/konuyu tanımla. Somut verilerle.
- **Paragraf 2:** Tezini tek cümle ile net söyle.
- **Paragraf 3:** Bu makalenin ne yapacağını söyle (model + veri + karşı argümanlar).

### 2. Ana içerik
- Önce model/çerçeve (okuyucu bağlamı anlamalı)
- Sonra kanıtlar/argümanlar (en objektif → en spekülatif sırasıyla)
- Olaylar ve yorumlar ayrı (kronoloji vs yorum karışmamalı)

### 3. Karşı argümanlar
- Kanıtlardan hemen sonra, sonuçtan önce
- "Neden yanılıyor olabilirim?" formatında
- Confirmation bias hissini azaltır

### 4. Sonuç (kısa ve güçlü)
- Tezi tekrar et
- Belirsizliği kabul et
- Takip edilmesi gereken sinyalleri ver

## SEO Kuralları

### Başlık
- Ana anahtar kelime başta olmalı
- 60 karakter altında
- Soru formatı tercih edilir (örn: "X Neden Y? Z Analizi")
- Yıl ekle (2026)

### Meta Description
- 150-160 karakter
- Ana anahtar kelimeyi içermeli
- Tıklama merak uyandırmalı
- `meta_desc` alanına yaz

### URL Slug
- Türkçe karakterler olabilir ama kısa tut
- Ana anahtar kelimeyi içermeli
- Format: `konu-analiz-tipi` (örn: `bitcoin-wyckoff-birikim-analizi`)

### İlk 100 Kelime
Şu anahtar kelimelerin en az 2-3'ü doğal şekilde geçmeli:
- Ana anahtar kelime (örn: "bitcoin neden düşüyor")
- Konu varyasyonu (örn: "bitcoin düşüşü")
- Analiz türü (örn: "bitcoin analiz")

### Alt Başlıklar (H2/H3)
- SEO uyumlu, soru formatında tercih edilir
- Örnek: "X Modeline Uyuyor mu?" yerine sadece "X Modeli"
- Featured snippet için net cevap paragrafı ekle

### Featured Snippet Paragrafı
Son bölümde Google'ın "kısa cevap" olarak gösterebileceği özet paragraf ekle:
> [Konu]'nun ana nedeni [X], [Y] ve [Z] olabilir. [Model]'e göre bu tür [olaylar], [sonuç]'tan önce görülebilir.

### İç ve Dış Linkler
- Varsa mirat.dev'deki ilgili yazılara link ver
- Dış linkler güvenilir kaynaklara (CoinDesk, Bloomberg, Fed, White House vb.)
- Her dış link açıklayıcı anchor text ile

## Yazım Kuralları

### Dil ve Ton
- Kısa cümleler (15-20 kelime ideal)
- Samimi ama profesyonel
- Spekülatif kısımları açıkça etiketle
- Jargon ilk geçtiği yerde tek cümle ile tanımla
- "Büyük oyuncular", "whale" gibi terimleri aç

### Explicit Yazım
- Her cümlede ara adımları atla**ma**. Okuyucu A'dan C'ye nasıl geldiğini anlamalı.
- Nedensellik zincirlerini açıkça yaz: "X oldu → bu Y'ye neden oldu → çünkü Z"
- İmplicit bilgiyi açık et: "BTC borsalarla beraber düştü" yerine "BTC artık geleneksel borsalarla aynı yönde hareket ettiği için beraber düştü"

### Kaçınılacaklar
- Aynı tezi 3'ten fazla yerde tekrarlama
- Uzun, dolambaçlı girişler
- Emoji
- Pasif yapı
- Gereksiz övgüler

## Lektor Dosya Formatı

```
title: [SEO uyumlu başlık]
---
body:

[Makale içeriği - Markdown]
---
meta_desc: [150-160 karakter meta description]
---
pub_date: [YYYY-MM-DD]
---
has_code: [yes/no]
---
tags: [uygun tag]
---
language: [tr/en]
```

Dosya yolu: `content/articles/[slug]/contents.lr`

## Kontrol Listesi

Makale tamamlandığında şunları kontrol et:

- [ ] Başlıkta ana anahtar kelime var mı?
- [ ] İlk 100 kelimede 2-3 anahtar kelime geçiyor mu?
- [ ] Meta description 150-160 karakter mi?
- [ ] Alt başlıklar SEO uyumlu mu?
- [ ] Teknik terimler ilk geçtiği yerde tanımlı mı?
- [ ] Spekülatif kısımlar etiketli mi?
- [ ] Karşı argümanlar kanıtlardan sonra mı?
- [ ] Featured snippet paragrafı var mı?
- [ ] Tüm linkler çalışıyor mu?
- [ ] `lektor build` başarılı mı?
