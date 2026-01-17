{assign var='popular_categories' value=[
  ['id' => 13, 'link_rewrite' => 'raspberry-pi', 'name' => 'RASPBERRY PI', 'image' => 'raspberry-pi.jpg'],
  ['id' => 14, 'link_rewrite' => 'warsztat', 'name' => 'WARSZTAT', 'image' => 'warsztat.jpg'],
  ['id' => 3, 'link_rewrite' => 'arduino', 'name' => 'ARDUINO', 'image' => 'arduino.jpg'],
  ['id' => 45, 'link_rewrite' => 'robotyka', 'name' => 'Robotyka', 'image' => 'robotyka.jpg'],
  ['id' => 124, 'link_rewrite' => 'oscyloskopy', 'name' => 'Oscyloskopy', 'image' => 'oscyloskopy.jpg'],
  ['id' => 35, 'link_rewrite' => 'drukarki-3d', 'name' => 'Drukarki 3D', 'image' => 'drukarki-3d.jpg']
]}

<div class="topcategory-container block-shadow">
  <div class="tapcategory-block">
    <h2 class="home-title">{l s='Popularne kategorie' d='Shop.Theme.Catalog'}</h2>
  </div>

  <div class="top_catlink owl-carousel owl-theme">
    {foreach from=$popular_categories item=category}
      <div class="category-item item">
        <a href="{$link->getCategoryLink($category.id, $category.link_rewrite)}">
          <div class="topcat_img">
            <img src="{$urls.base_url}themes/kamami/assets/img/categories/{$category.image}"
              title="{$category.name|escape:'html':'UTF-8'}" width="217" height="217" loading="lazy"
              alt="{$category.name|escape:'html':'UTF-8'}">
          </div>
          <div class="cat_name">{$category.name|escape:'html':'UTF-8'}</div>
        </a>
      </div>
    {/foreach}
  </div>
</div>