<article class="card">
  <div class="banner" style="<?= banner_style($p) ?>"><span><?= e($p['destination']) ?></span></div>
  <div class="body">
    <h3><?= e($p['title']) ?></h3>
    <p><?= e($p['summary']) ?></p>
    <p class="meta"><?= (int)$p['days'] ?> days · <?= e($p['category']) ?> · <?= e($p['country']) ?></p>
    <div class="row"><strong><?= inr($p['price']) ?> <small>per person</small></strong>
    <a class="btn small" href="package.php?id=<?= (int)$p['id'] ?>">View</a></div>
  </div>
</article>
