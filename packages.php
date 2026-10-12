<?php $pageTitle = 'Packages'; include 'includes/header.php';
$q = trim($_GET['q'] ?? ''); $cat = $_GET['category'] ?? ''; $reg = $_GET['region'] ?? '';
$sql = 'SELECT * FROM packages WHERE 1'; $args = [];
if ($q !== '') { $sql .= ' AND (title LIKE ? OR destination LIKE ? OR country LIKE ?)'; array_push($args, "%$q%", "%$q%", "%$q%"); }
if ($cat !== '') { $sql .= ' AND category = ?'; $args[] = $cat; }
if ($reg !== '') { $sql .= ' AND region = ?'; $args[] = $reg; }
$st = db()->prepare($sql . ' ORDER BY region = "International", region, price'); $st->execute($args); $rows = $st->fetchAll(); ?>
<section class="wrap">
  <h1>Tour packages</h1>
  <form method="get" class="search inline">
    <input name="q" value="<?= e($q) ?>" placeholder="Search place or country" aria-label="Search">
    <select name="region" aria-label="Region"><option value="">All regions</option>
      <?php foreach (REGIONS as $r): ?><option value="<?= e($r) ?>" <?= $reg===$r?'selected':'' ?>><?= $r === 'International' ? 'Abroad' : e($r) . ' India' ?></option><?php endforeach; ?></select>
    <select name="category" aria-label="Category"><option value="">All types</option>
      <?php foreach (CATEGORIES as $c): ?><option <?= $cat===$c?'selected':'' ?>><?= $c ?></option><?php endforeach; ?></select>
    <button class="btn">Filter</button>
  </form>
  <p class="meta"><?= count($rows) ?> trips found</p>
  <?php if (!$rows): ?><p class="empty">No trips match that search. Clear the filters to see everything.</p><?php endif; ?>
  <div class="grid"><?php foreach ($rows as $p) include 'includes/card.php'; ?></div>
</section>
<?php include 'includes/footer.php'; ?>
