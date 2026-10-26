# Kaynaklar ve içerik kökeni

Rapor ve çalışma kaynakları bu depodadır. Haricî PHP, Wiz, Calif, watchTowr, AWS, Ubuntu, CyberPanel ve Docker yayınları aşağıdaki bağlantılarla kaynak gösterilir; tam kopyaları veya container imajları depoda dağıtılmaz. İlgili üçüncü taraf lisansı ayrıca geçerlidir.

## 23. Kaynaklar

Erişim ve teknik bilgi kesim tarihi 25 Ekim 2026'dır. Tam URL'ler basılı nüsha için korunmuştur. Birincil duyurular, sağlayıcı açıklamaları ve içerik kontrolü yapılamayan topluluk materyalleri aşağıda ayrılmıştır.

**[1] PHP Project 2026 güvenlik ve ek oturum duyuruları.** 21 Ekim yama eşikleri ve 23 Ekim ek uyarısı.  
https://www.php.net/archive/2026.php

**[2] PHP GHSA w8hw w9fx j79w.** CVE-2026-109618 için resmî OOM bülteni.  
https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w

**[3] PHP GHSA 6wmf 4rv5 p3rp.** CVE-2026-109619 için resmî stale-state bülteni.  
https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp

**[4] Wiz Research PHP2Shell araştırması.** 21 Ekim 2026; kök neden, gösterilen etkiler ve düzeltme çalışmaları.  
https://www.wiz.io/blog/php2shell-php-rce

**[5] Calif Research PHP2Shell.** Birincil araştırmacı anlatımı ve bildirim zaman çizelgesi.  
https://calif.io/php2shell/

**[6] ikow php2shell poc tespit dizini.** Topluluk materyali; ürün uyumluluğu ve kapsamı bağımsız olarak doğrulanmadı. Kural içeriği, sayısı, lisansı ve uyumluluğu uygulanmadan önce kontrol edilmelidir.  
https://github.com/ikow/php2shell-poc/tree/main/detection

**[7] MITRE CWE 825.** Geçersiz veya ömrü dolmuş işaretçinin kullanımı için kavramsal başvuru.  
https://cwe.mitre.org/data/definitions/825.html

**[8] PHP oturum yapılandırma kılavuzu.** session.serialize_handler ve ilgili ayarların başvuru belgesi.  
https://www.php.net/manual/en/session.configuration.php

**[9] watchTowr PHP2Shell FAQ.** 23 Ekim güncellemeli araştırmacı yayını; 21 Ekim honeypot gözlemi ve açıklama süreci.  
https://watchtowr.com/intelligence/php-cve-2026-109618-faq/

**[10] AWS Security Blog MadPot gözlemi.** 21 Ekim 2026; 17 Ekim tarihine uzanan girişimin geriye dönük telemetri analizi.  
https://aws.amazon.com/blogs/security/amazon-threat-intelligence-identifies-php2shell-exploitation-prior-to-public-disclosure-in-madpot/

**[11] Ubuntu USN 8948 1.** 21 Ekim 2026; desteklenen Ubuntu paketlerindeki düzeltme sürümleri.  
https://ubuntu.com/security/notices/USN-8948-1

**[12] Ubuntu USN 8948 2.** 21 Ekim 2026; eski Ubuntu sürümleri için Pro ve Legacy destek kapsamı.  
https://ubuntu.com/security/notices/USN-8948-2

**[13] CyberPanel güvenlik yanıtı ve test planı.** 24 Ekim güncellemeli üretici kaydı; eşleşen OPcache ve ayrı panel runtime doğrulaması.  
https://cyberpanel.net/blog/php-security-october-2026-cyberpanel-response

**[14] Docker resmî PHP imajı.** İmaj ailesi için başvuru; bu rapor belirli etiketlerin çekildiği iddiasını taşımaz.  
https://hub.docker.com/_/php

**[15] Docker bridge ağ belgesi.** Ağ davranışı ve izolasyon yapılandırması için başvuru.  
https://docs.docker.com/engine/network/drivers/bridge/

**[16] PHP FPM yapılandırma kılavuzu.** Havuz, worker ve pm.max_requests parametreleri için başvuru.  
https://www.php.net/manual/en/install.fpm.configuration.php

### Kullanım ve yayın kapsamı

Bu rapordaki uygulamalar ayrılmış ve yetkilendirilmiş laboratuvar ortamında yürütülür. Üçüncü taraf kaynakların kendi lisansları geçerlidir. Bu derleme için ayrıca bir açık lisans atanmamıştır.

