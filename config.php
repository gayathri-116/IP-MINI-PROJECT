<?php
// ---- Edit these to match your MySQL setup ----
const DB_HOST = 'localhost';
const DB_NAME = 'wanderly';
const DB_USER = 'root';
const DB_PASS = '';

session_start();

function db(): PDO {
    static $pdo = null;
    if (!$pdo) {
        $pdo = new PDO('mysql:host=' . DB_HOST . ';dbname=' . DB_NAME . ';charset=utf8mb4', DB_USER, DB_PASS,
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
    }
    return $pdo;
}
function e($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
function inr($n) { return '₹' . number_format((float)$n); }
function logged_in() { return isset($_SESSION['uid']); }
function require_login() { if (!logged_in()) { header('Location: login.php?next=' . urlencode($_SERVER['REQUEST_URI'])); exit; } }
function require_admin() { require_login(); if (($_SESSION['role'] ?? '') !== 'admin') { http_response_code(403); exit('Admins only.'); } }
function csrf() { return $_SESSION['csrf'] ??= bin2hex(random_bytes(16)); }
function check_csrf() { if (!hash_equals($_SESSION['csrf'] ?? '', $_POST['csrf'] ?? '')) exit('Invalid form token.'); }

const CATEGORIES = ['Nature','Heritage','Adventure','Beach','City','Spiritual','Wildlife'];
const REGIONS = ['North','South','East','West','Central','North-East','Islands','International'];
function slugify($s) { return trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($s)), '-'); }
function theme($region) {
    $t = ['North'=>['#4f7cac','#16243a'],'South'=>['#1b8a8f','#0d3b4a'],'East'=>['#7a5ea8','#2b1f45'],'West'=>['#e0a030','#6b3a12'],
          'Central'=>['#5c8a4d','#1f3a1c'],'North-East'=>['#2f9e7a','#0f3a2c'],'Islands'=>['#12a3a3','#0a3d62'],'International'=>['#c8553d','#3a1a2e']];
    return $t[$region] ?? ['#1b8a8f','#12263a'];
}
// Gallery images: files in assets/img/<slug>/ come first, then keyword photos from loremflickr.
function pkg_images(array $p, int $n = 4): array {
    $slug = slugify($p['title']); $imgs = [];
    foreach (glob(__DIR__ . "/assets/img/$slug/*.{jpg,jpeg,png,webp,svg}", GLOB_BRACE) ?: [] as $f) $imgs[] = "assets/img/$slug/" . basename($f);
    $kw = str_replace(' ', '', $p['keywords'] ?: $p['destination']);
    for ($i = 1; count($imgs) < $n; $i++) $imgs[] = "https://loremflickr.com/900/600/$kw/all?lock=" . ($p['id'] * 10 + $i);
    return $imgs;
}
function banner_style(array $p): string {
    [$a, $b] = theme($p['region']); $img = pkg_images($p, 1)[0];
    return "background-image:linear-gradient(to top,rgba(0,0,0,.7),transparent 65%),url('" . e($img) . "'),linear-gradient(135deg,$a,$b)";
}
