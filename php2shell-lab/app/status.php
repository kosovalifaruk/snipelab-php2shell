<?php
declare(strict_types=1);
header('Content-Type: application/json');
header('Cache-Control: no-store');
function flag_value(string $name): bool {
    return filter_var(ini_get($name), FILTER_VALIDATE_BOOLEAN);
}
echo json_encode([
    'lab' => 'SnipeLab-PHP2Shell',
    'php_version' => PHP_VERSION,
    'sapi' => PHP_SAPI,
    'pid' => getmypid(),
    'ini_file' => php_ini_loaded_file(),
    'ini_scanned' => php_ini_scanned_files(),
    'upload_progress' => flag_value('session.upload_progress.enabled'),
    'fatal_backtraces' => flag_value('fatal_error_backtraces'),
    'memory_limit' => ini_get('memory_limit'),
    'opcache_version' => phpversion('Zend OPcache') ?: null
], JSON_UNESCAPED_SLASHES | JSON_THROW_ON_ERROR);
