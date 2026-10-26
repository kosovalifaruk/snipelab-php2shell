<?php
declare(strict_types=1);
header('Content-Type: application/json');
header('Cache-Control: no-store');
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit;
}
$file = $_FILES['probe'] ?? null;
if (!$file || $file['error'] !== UPLOAD_ERR_OK || $file['size'] > 4096
    || !is_uploaded_file($file['tmp_name'])) {
    http_response_code(400);
    echo json_encode(['accepted' => false]);
    exit;
}
echo json_encode([
    'accepted' => true,
    'size' => $file['size'],
    'sha256' => hash_file('sha256', $file['tmp_name']),
    'persisted' => false
], JSON_THROW_ON_ERROR);
// No move_uploaded_file(): PHP removes the temporary upload at shutdown.
