<?php
declare(strict_types=1);
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit;
}
header('Content-Type: application/json');
ini_set('memory_limit', '16M');
error_log('LAB_BOUNDED_OOM_DEMO pid=' . getmypid());
// One fixed allocation; no size is accepted from the HTTP request.
$bounded = str_repeat('L', 24 * 1024 * 1024);
echo json_encode(['oom_observed' => false, 'allocated' => strlen($bounded)]);
