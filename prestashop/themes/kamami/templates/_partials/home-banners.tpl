{**
 * Home page side banners (displayed alongside the slider)
 * Layout: 2 small banners stacked on left + 1 tall banner on right
 *}

<div id="xibanner-col-displaySliderAd" class="xibanner-columns xibanner-col-3">

  {* Left column: banners 1 and 2 stacked *}
  <div class="xibanner-column xibanner-combine-3">
    <div class="col-align-left">
      <div class="baneritem-1">
        <a href="{$urls.base_url}content/1-dostawa-i-platnosc" class="item-link"
          onclick="return !window.open(this.href);">
          <img src="{$urls.base_url}themes/kamami/assets/img/banners/darmowa-dostawa.jpg"
            data-original="{$urls.base_url}themes/kamami/assets/img/banners/darmowa-dostawa.jpg"
            class="item-img js-lazyload" loading="lazy" width="355" height="317" alt="Darmowa dostawa"
            style="width: 100%;">
        </a>
      </div>
    </div>

    <div class="xibanner-column xibanner-combine-3">
      <div class="baneritem-2">
        <a href="#" class="item-link" onclick="return !window.open(this.href);">
          <img src="{$urls.base_url}themes/kamami/assets/img/banners/banner-promo.jpg"
            data-original="{$urls.base_url}themes/kamami/assets/img/banners/banner-promo.jpg"
            class="item-img js-lazyload" loading="lazy" width="355" height="317" alt="Promocja" style="width: 100%;">
        </a>
      </div>
    </div>
  </div>

  {* Right column: tall banner 3 *}
  <div class="xibanner-column xibanner-combine-3">
    <div class="col-align-right">
      <div class="baneritem-3">
        <a href="#" class="item-link">
          <img src="{$urls.base_url}themes/kamami/assets/img/banners/banner-tall.jpg"
            data-original="{$urls.base_url}themes/kamami/assets/img/banners/banner-tall.jpg"
            class="item-img js-lazyload" loading="lazy" width="355" height="640" alt="Banner boczny"
            style="width: 100%;">
        </a>
      </div>
    </div>
  </div>

</div>