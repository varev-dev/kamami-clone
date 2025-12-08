{**
 * Custom banners for left column
 * Configure banners in the $banners array below
 * 
 * Properties:
 * - id: Banner ID (used for baneritem-{id} class)
 * - url: Link destination URL
 * - image: Image filename (images should be placed in themes/kamami/assets/img/banners/)
 * - alt: Alt text for the image
 * - width: Image width in pixels
 * - height: Image height in pixels
 * - target: Link target ('_blank' for new window, '_self' for same window, or empty for default)
 *}
{assign var="banners" value=[
  [
    'id' => 1,
    'url' => 'https://kamami.pl/analizatory-sieci/1186078-tinysa-analizator-sieci-100khz-960mhz-z-wyswietlaczem-28-5906623452354.html',
    'image' => '2c21ea6ded7817f60fde477bcc6a3965ad7be530_1186078_PROMO.jpg',
    'alt' => 'Promocja tygodniowa',
    'width' => 800,
    'height' => 800,
    'target' => '_blank'
  ],
  [
    'id' => 2,
    'url' => 'https://kamami.pl/15238-raspberry-pi',
    'image' => '12481aeaae26a25ba9b1d05f5064a77a9c650a12_DIGITAL APPROVED RESELLER LOGO_COLOUR.png',
    'alt' => 'Raspberry Pi Approved Reseller',
    'width' => 2540,
    'height' => 591,
    'target' => ''
  ],
  [
    'id' => 3,
    'url' => 'https://www.st.com/content/st_com/en/partner/partner-program/partnerpage/Kamami.html',
    'image' => 'e045696cdf0884bf79b533b2e5633debe38b4ea2_st_logo_220.png',
    'alt' => 'ST Authorized Partner',
    'width' => 220,
    'height' => 110,
    'target' => ''
  ]
]}

<div id="xibanner-col-displayLeftColumn" class="xibanner-columns xibanner-col-3">
  {foreach from=$banners item=banner}
    <div class="xibanner-column xibanner-combine-3">
      <div class="baneritem-{$banner.id}">
        <a href="{$banner.url}" class="item-link" {if $banner.target} target="{$banner.target}" {/if}>
          <img src="{$urls.base_url}themes/kamami/assets/img/banners/{$banner.image}"
            data-original="{$urls.base_url}themes/kamami/assets/img/banners/{$banner.image}"
            class="item-img image-fluid js-lazyload" loading="lazy" width="{$banner.width}" height="{$banner.height}"
            alt="{$banner.alt}" style="width: 100%;" />
        </a>
      </div>
    </div>
  {/foreach}
</div>