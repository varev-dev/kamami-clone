{**
 * Popular Categories carousel component
 * Displays featured categories with images in an Owl Carousel
 *}

{* Define the popular categories - in a real setup, this would come from a module or database *}
{assign var='popular_categories' value=[
  ['name' => 'RASPBERRY PI', 'link' => "{$urls.base_url}6-akcesoria", 'image' => 'raspberry-pi.jpg'],
  ['name' => 'ARDUINO', 'link' => "{$urls.base_url}6-akcesoria", 'image' => 'arduino.jpg'],
  ['name' => 'Robotyka', 'link' => "{$urls.base_url}6-akcesoria", 'image' => 'robotyka.jpg'],
  ['name' => 'WARSZTAT', 'link' => "{$urls.base_url}6-akcesoria", 'image' => 'warsztat.jpg'],
  ['name' => 'Drukarki 3D', 'link' => "{$urls.base_url}6-akcesoria", 'image' => 'drukarki-3d.jpg'],
  ['name' => 'Oscyloskopy', 'link' => "{$urls.base_url}6-akcesoria", 'image' => 'oscyloskopy.jpg']
]}

<div class="topcategory-container block-shadow">
  <div class="tapcategory-block">
    <h2 class="home-title">{l s='Popularne kategorie' d='Shop.Theme.Catalog'}</h2>
  </div>

  <div class="top_catlink owl-carousel owl-theme">
    {foreach from=$popular_categories item=category}
      <div class="category-item item">
        <a href="{$category.link}">
          <div class="topcat_img">
            <img src="{$urls.base_url}themes/kamami/assets/img/categories/{$category.image}"
                 title="{$category.name}"
                 width="217"
                 height="217"
                 loading="lazy"
                 alt="{$category.name}">
          </div>
          <div class="cat_name">{$category.name}</div>
        </a>
      </div>
    {/foreach}
  </div>
</div>

