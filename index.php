<?php $pageTitle = 'Home'; include 'includes/header.php';
$india = db()->query("SELECT * FROM packages WHERE country='India' ORDER BY RAND() LIMIT 3")->fetchAll();
$world = db()->query("SELECT * FROM packages WHERE region='International' ORDER BY RAND() LIMIT 3")->fetchAll();
$total = db()->query('SELECT COUNT(*) FROM packages')->fetchColumn(); ?>
<section class="hero">
  <h1>Every corner of India.<br>And the world beyond.</h1>
  <p><?= (int)$total ?> hand-planned trips, from Ladakh to Lakshadweep to Lisbon, with hotels, transfers and guides included.</p>
  <form action="packages.php" method="get" class="search">
    <input name="q" placeholder="Where to? Try Goa, Sikkim, Bali, Dubai" aria-label="Destination">
    <select name="category" aria-label="Trip type"><option value="">Any trip type</option>
      <?php foreach (CATEGORIES as $c): ?><option><?= $c ?></option><?php endforeach; ?></select>
    <button class="btn">Find trips</button>
  </form>
</section>
<section class="wrap">
  <h2>Browse by region</h2>
  <div class="chips"><?php foreach (REGIONS as $r): ?><a class="chip" href="packages.php?region=<?= urlencode($r) ?>"><?= $r === 'International' ? 'Abroad' : e($r) . ' India' ?></a><?php endforeach; ?></div>
  <h2>Popular in India</h2>
  <div class="grid"><?php foreach ($india as $p) include 'includes/card.php'; ?></div>
  <h2>Popular abroad</h2>
  <div class="grid"><?php foreach ($world as $p) include 'includes/card.php'; ?></div>
  <p><a class="btn ghost" href="packages.php">See all packages</a></p>
</section>
<section class="wrap steps">
  <h2>How booking works</h2>
  <ol>
    <li><b>Choose</b> a package and look through its photos and itinerary.</li>
    <li><b>Book</b> with your travel date and group size. The total updates as you type.</li>
    <li><b>Track</b> the status of every booking under My bookings.</li>
  </ol>
</section>
<?php include 'includes/footer.php'; ?>
