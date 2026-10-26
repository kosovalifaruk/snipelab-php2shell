# Katkı ve değişiklik doğrulaması

1. Değişikliğin teknik gerekçesini ve etkilediği dosyaları açıklayın.
2. `python3 -m unittest discover -s php2shell-lab/tests -v` çalıştırın. Fixture portları boş olmalıdır.
3. Runtime kodunu değiştirirseniz raporun Markdown kaynak ekini, PDF yayınını ve VALIDATION kaydını aynı sürüm için güncelleyin. Yeni test sonucu elde edilmeden ölçülmüş başarı yazmayın.
4. `python3 tools/update_checksums.py` ardından `python3 tools/verify_release.py` çalıştırın.
5. Gerçek Docker/PHP sonucu varsa işletim sistemi, imaj digest'leri, SAPI ve test kapsamını belirtin. Hassas kanıtları pull request'e eklemeyin.

Katkı kabulünün lisans koşulları ayrıca tanımlanmamıştır; kapsam için LICENSING.md dosyasını okuyun.
