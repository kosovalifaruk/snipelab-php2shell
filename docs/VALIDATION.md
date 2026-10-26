# Doğrulama durumu

Paket 3.0.4; rapor ve runtime 3.0. Paket tarihi: 26 Ekim 2026.

- Kontrol testlerinin 8/8 sonucu validation/tests içindedir; bu kayıtlar fixture testlerine aittir.
- Repo bütünlük, kaynak eşlemesi ve Markdown yerel bağlantı kontrolleri yeniden çalıştırıldı ve geçti.
- Python derleme ve 8/8 fixture testi yeniden yürütüldü.
- İki workflow YAML yapısı ve içerdiği shell komutlarının sözdizimi yerelde doğrulandı. Readiness yardımcısı beş canlı localhost fixture üzerinde geçti. GitHub Actions çalıştırma sonucu henüz doğrulanmadı.
- Docker/PHP/Nginx gerçek runtime kontrolü beklemektedir. Runtime verification workflow'u bu işi operatör tarafından başlatılabilir hale getirir.
- İmaj çekilemezse veya gerçek kontrol başarısızsa workflow başarısız olur; yerine başka sürüm seçilmez.

Detaylı ilk kayıt: [Laboratuvar doğrulama tablosu](../php2shell-lab/VALIDATION.md).

Kontrol sonuçları kendi kapsamları içinde yorumlanır. Runtime sonucu alınmadan gerçek PHP çalıştırmasının veya bağımsız CVE sömürüsünün doğrulandığı ileri sürülmez.

Paket kontrol özeti: [package-checks.json](../validation/tests/package-checks.json).
