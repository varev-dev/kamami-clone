{**
 * Copyright since 2007 PrestaShop SA and Contributors
 * PrestaShop is an International Registered Trademark & Property of PrestaShop SA
 *
 * NOTICE OF LICENSE
 *
 * This source file is subject to the Academic Free License 3.0 (AFL-3.0)
 * that is bundled with this package in the file LICENSE.md.
 * It is also available through the world-wide-web at this URL:
 * https://opensource.org/licenses/AFL-3.0
 * If you did not receive a copy of the license and are unable to
 * obtain it through the world-wide-web, please send an email
 * to license@prestashop.com so we can send you a copy immediately.
 *
 * DISCLAIMER
 *
 * Do not edit or add to this file if you wish to upgrade PrestaShop to newer
 * versions in the future. If you wish to customize PrestaShop for your
 * needs please refer to https://devdocs.prestashop.com/ for more information.
 *
 * @author    PrestaShop SA and Contributors <contact@prestashop.com>
 * @copyright Since 2007 PrestaShop SA and Contributors
 * @license   https://opensource.org/licenses/AFL-3.0 Academic Free License 3.0 (AFL-3.0)
 *}
{extends file='page.tpl'}

{block name='page_content_container'}
  <section id="content" class="page-home">
    {block name='page_content_top'}{/block}

    {block name='page_content'}
      {* Home content top: Slider + Side banners *}
      {block name='home_content_top'}
        <div class="home-content-top">
          <div class="row">
            {* Left side: Image slider *}
            <div class="col-sm-12 col-md-12 col-lg-6 side-slide4">
              {hook h='displayHome' mod='ps_imageslider'}
            </div>

            {* Right side: Promotional banners *}
            <div class="col-sm-12 col-md-12 col-lg-6 side-adv4">
              {include file='_partials/home-banners.tpl'}
            </div>
          </div>
        </div>
      {/block}

      {* Rest of home page content (featured products, etc.) *}
      {block name='hook_home'}
        {hook h='displayHome' excl='ps_imageslider'}
      {/block}
    {/block}
  </section>
{/block}