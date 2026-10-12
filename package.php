<?php $pageTitle = 'Package'; include 'includes/header.php';
$st = db()->prepare('SELECT * FROM packages WHERE id=?'); $st->execute([(int)($_GET['id'] ?? 0)]); $p = $st->fetch();
if (!$p) { echo '<section class="wrap"><p class="empty">That package does not exist. <a href="packages.php">Browse packages</a></p></section>'; include 'includes/footer.php'; exit; }
$errors = []; $done = false;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    require_login(); check_csrf();
    $date = $_POST['travel_date'] ?? ''; $n = (int)($_POST['travellers'] ?? 0);
    if (!$date || strtotime($date) < strtotime('tomorrow')) $errors[] = 'Choose a travel date from tomorrow onwards.';
    if ($n < 1 || $n > 20) $errors[] = 'Travellers must be between 1 and 20.';
    if (!$errors) {
        db()->prepare('INSERT INTO bookings (user_id,package_id,travel_date,travellers,total) VALUES (?,?,?,?,?)')
            ->execute([$_SESSION['uid'], $p['id'], $date, $n, $p['price'] * $n]);
        header('Location: my_bookings.php?booked=1'); exit;
    }
} ?>
<section class="wrap detail">
  <div>
    <?php $imgs = pkg_images($p, 4); [$c1, $c2] = theme($p['region']); ?>
    <div class="gallery">
      <div class="main" style="background:linear-gradient(135deg,<?= e($c1) ?>,<?= e($c2) ?>)">
        <img id="mainImg" src="<?= e($imgs[0]) ?>" alt="<?= e($p['destination']) ?>" onerror="this.style.visibility='hidden'">
      </div>
      <div class="thumbs"><?php foreach ($imgs as $i => $im): ?>
        <button type="button" class="thumb <?= $i===0?'active':'' ?>" data-src="<?= e($im) ?>" aria-label="Photo <?= $i+1 ?>"><img src="<?= e($im) ?>" alt="" loading="lazy" onerror="this.style.visibility='hidden'"></button>
      <?php endforeach; ?></div>
    </div>
    <h1><?= e($p['title']) ?></h1>
    <p class="meta"><?= (int)$p['days'] ?> days · <?= e($p['category']) ?> · <?= e($p['destination']) ?>, <?= e($p['country']) ?></p>
    <p><?= e($p['summary']) ?></p>
    <h2>Itinerary and inclusions</h2>
    <p><?= nl2br(e($p['details'])) ?></p>
    <p class="meta">Every package includes hotels, breakfast, local transfers and a trip coordinator. Flights are extra for international trips.</p>
  </div>
  <aside class="panel">
    <h2>Book this trip</h2>
    <p><strong><?= inr($p['price']) ?></strong> per person</p>
    <?php foreach ($errors as $er): ?><p class="error"><?= e($er) ?></p><?php endforeach; ?>
    <?php if (!logged_in()): ?>
      <p><a class="btn" href="login.php?next=<?= urlencode($_SERVER['REQUEST_URI']) ?>">Log in to book</a></p>
    <?php else: ?>
    <form method="post" id="bookForm" data-price="<?= (float)$p['price'] ?>">
      <input type="hidden" name="csrf" value="<?= csrf() ?>">
      <label>Travel date <input type="date" name="travel_date" required min="<?= date('Y-m-d', strtotime('+1 day')) ?>"></label>
      <label>Travellers <input type="number" name="travellers" value="2" min="1" max="20" required></label>
      <p class="total">Total: <strong id="total"><?= inr($p['price'] * 2) ?></strong></p>
      <button class="btn">Confirm booking</button>
    </form>
    <?php endif; ?>
  </aside>
</section>
<?php include 'includes/footer.php'; ?>
