{**
 * Override of ps_brandlist module template
 * Custom Owl Carousel implementation for brand display
 *}

{if $brands}
  <div class="dfx_manufacturer manufacturer-carousel owl-carousel owl-theme revealOnScroll" data-animation="fadeInUp"
    data-timeout="10">
    {foreach from=$brands item=brand}
      <div class="image_manufacture">
        <a href="{$brand.link}" title="{$brand.name}" aria-label="{$brand.name}">
          {if $brand.image|is_numeric}
            {* Image exists - use manufacturer_default type to match HTML format *}
            <img class="img-fluid" loading="lazy"
              src="{$link->getManufacturerImageLink($brand.id_manufacturer, 'manufacturer_default')}" alt="{$brand.name}"
              width="129" height="89">
          {else}
            {* No image - show placeholder or skip *}
            <div class="brand-placeholder"
              style="width: 129px; height: 89px; display: flex; align-items: center; justify-content: center; background: #f5f5f5; border: 1px solid #ddd;">
              <span style="color: #999; font-size: 12px;">{$brand.name}</span>
            </div>
          {/if}
        </a>
      </div>
    {/foreach}
  </div>
{else}
  {* No brands *}
{/if}