# SnipeLab sürüm 3.0 doğrulama kaydı

Kontrol tarihi: 25 Ekim 2026. Bu kayıt kontrol testlerine aittir.

| İşlem | Gerçek durum |
|---|---|
| Python sözdizimi / derleme | GEÇTİ |
| Yerel HTTP sözleşme testleri | 8/8 GEÇTİ; beş gerçek localhost HTTP fixture'ı |
| Compose YAML ayrıştırma | GEÇTİ; PyYAML ile |
| Yapısal ağ / port / dosya / kaynak kontrolleri | GEÇTİ |
| Kavramsal yaşam döngüsü modeli | GEÇTİ; geçersiz/eski referans invariantı ve reset sonrası düzelme |
| docker compose config (Docker uygulamasıyla) | ÇALIŞTIRILMADI; Docker yok |
| İmaj çekme / RepoDigest / konteyner başlatma | ÇALIŞTIRILMADI; Docker yok |
| PHP -l / gerçek Apache ve FPM istekleri | ÇALIŞTIRILMADI; PHP ve Docker yok |
| Nginx sözdizimi kontrolü | ÇALIŞTIRILMADI; runtime yok |
| Gerçek PHP OOM günlük korelasyonu | ÇALIŞTIRILMADI |
| WAF / IDS / SIEM alarmı | ÇALIŞTIRILMADI; sensör pakette yok |
| Gerçek CVE UAF / bellek okuma / RCE | BU PAKETTE SINANMIYOR |

Fixture testi PHP motoru değildir. Yapısal YAML kontrolü Docker Compose doğrulamasının yerine geçmez. README'deki operatör kabul adımları tamamlanmadan gerçek PHP deneyleri için PASS raporlanmaz.
