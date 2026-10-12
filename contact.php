<?php $pageTitle = 'Contact'; include 'includes/header.php';
$errors = []; $sent = false;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    check_csrf();
    $n = trim($_POST['name'] ?? ''); $m = trim($_POST['email'] ?? ''); $t = trim($_POST['message'] ?? '');
    if ($n === '' || $t === '') $errors[] = 'Name and message are required.';
    if (!filter_var($m, FILTER_VALIDATE_EMAIL)) $errors[] = 'Enter a valid email address.';
    if (!$errors) { db()->prepare('INSERT INTO messages (name,email,message) VALUES (?,?,?)')->execute([$n,$m,$t]); $sent = true; }
} ?>
<section class="wrap narrow">
  <h1>Contact us</h1>
  <?php if ($sent): ?><p class="ok">Thanks, your message is saved. We'll reply by email.</p><?php endif; ?>
  <?php foreach ($errors as $er): ?><p class="error"><?= e($er) ?></p><?php endforeach; ?>
  <form method="post" class="stack">
    <input type="hidden" name="csrf" value="<?= csrf() ?>">
    <label>Name <input name="name" required></label>
    <label>Email <input type="email" name="email" required></label>
    <label>Message <textarea name="message" rows="5" required></textarea></label>
    <button class="btn">Send message</button>
  </form>
</section>
<?php include 'includes/footer.php'; ?>
