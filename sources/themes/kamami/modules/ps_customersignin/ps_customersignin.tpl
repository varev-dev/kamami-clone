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
<div id="_desktop_user_info" class="pull-right hover">
  {if $logged}
    <div class="account-dropdown account-logged">
      <div class="ajax-userinfo-src dropdown js-dropdown">
        <div class="hidden-sm-down account-login" data-toggle="dropdown" aria-expanded="false">
          <a class="account user-info" href="{$urls.pages.my_account}"
            title="{l s='View my customer account' d='Shop.Theme.Customeraccount'}" rel="nofollow">
            <span class="hidden-sm-down">{$customerName}</span>
          </a>
        </div>
        <a class="account-login hidden-md-up" href="#" data-toggle="dropdown"
          title="{l s='View my customer account' d='Shop.Theme.Customeraccount'}" rel="nofollow">
          <i class="redfox-user"></i>
        </a>
        <ul class="dropdown-menu">
          <li class="customer-name hidden-md-up"><span>{$customerName}</span></li>
          <li>
            <a href="{$urls.pages.my_account}" class="dropdown-item">
              <span>{l s='Your account' d='Shop.Theme.Customeraccount'}</span>
              <i class="redfox-user"></i>
            </a>
          </li>
          <li>
            <a href="{$urls.pages.identity}" class="dropdown-item">
              <span>{l s='Information' d='Shop.Theme.Customeraccount'}</span>
              <i class="redfox-information"></i>
            </a>
          </li>
          <li>
            <a href="{$urls.pages.address}" class="dropdown-item">
              <span>{l s='Add address' d='Shop.Theme.Customeraccount'}</span>
              <i class="material-icons add">&#xE145;</i>
            </a>
          </li>
          <li>
            <a href="{$urls.pages.history}" class="dropdown-item">
              <span>{l s='Order history and details' d='Shop.Theme.Customeraccount'}</span>
              <i class="material-icons event">&#xE878;</i>
            </a>
          </li>
          <li>
            <a href="{$urls.pages.discount}" class="dropdown-item">
              <span>{l s='Vouchers' d='Shop.Theme.Customeraccount'}</span>
              <i class="material-icons local_offer">&#xE54E;</i>
            </a>
          </li>
          <li></li>
          <li>
            <a href="{$urls.actions.logout}" class="dropdown-item sign-out">
              <span>{l s='Sign out' d='Shop.Theme.Actions'}</span>
              <i class="material-icons exit_to_app">&#xE879;</i>
            </a>
          </li>
          {if isset($languages) && isset($current_language)}
            <li class="sub-drop hidden-md-up">
              <ul id="abs-lang" class="pop-lang">
                {foreach from=$languages item=language}
                  <li class="lang-image {if $language.id_lang == $current_language.id_lang}current{/if}">
                    <a href="{url entity='language' id=$language.id_lang}" class="dropdown-item"
                      data-iso-code="{$language.iso_code}">
                      <img class="fl" src="/img/l/{$language.id_lang}.jpg" width="16" height="10"
                        style="width: 16px; height: auto;" alt="{$language.name_simple}" loading="lazy">
                      <span class="lang-text">{$language.name_simple}</span>
                    </a>
                  </li>
                {/foreach}
              </ul>
            </li>
          {/if}
          {if isset($currencies) && isset($current_currency)}
            <li class="sub-drop hidden-md-up">
              <ul id="abs-currency" class="pop-currency">
                {foreach from=$currencies item=currency}
                  <li {if $currency.current}class="current" {/if}>
                    <a title="{$currency.name}" rel="nofollow" href="{$currency.url}"
                      class="dropdown-item">{$currency.iso_code}</a>
                  </li>
                {/foreach}
              </ul>
            </li>
          {/if}
        </ul>
      </div>
    </div>
  {else}
    <div class="account-dropdown">
      <div class="ajax-userinfo-src dropdown js-dropdown">
        <div class="hidden-sm-down">
          <a href="{$urls.pages.my_account}" title="{l s='Sign in' d='Shop.Theme.Actions'}" rel="nofollow"
            class="user-info">
            <span class="hidden-sm-down"><i class="redfox-user"></i>{l s='Sign in' d='Shop.Theme.Actions'}</span>
          </a>
        </div>
        <a class="account-login hidden-md-up" href="#" data-toggle="dropdown"
          title="{l s='View my customer account' d='Shop.Theme.Customeraccount'}" rel="nofollow">
          <i class="redfox-user"></i>
        </a>
        <ul class="dropdown-menu hidden-md-up">
          <li>
            <a href="{$urls.pages.my_account}" class="dropdown-item">
              <span>{l s='Sign in' d='Shop.Theme.Actions'}</span>
              <i class="redfox-user"></i>
            </a>
          </li>
          {if isset($languages) && isset($current_language)}
            <li class="sub-drop">
              <ul id="abs-lang" class="pop-lang">
                {foreach from=$languages item=language}
                  <li class="lang-image {if $language.id_lang == $current_language.id_lang}current{/if}">
                    <a href="{url entity='language' id=$language.id_lang}" class="dropdown-item"
                      data-iso-code="{$language.iso_code}">
                      <img class="fl" src="/img/l/{$language.id_lang}.jpg" width="16" height="10"
                        style="width: 16px; height: auto;" alt="{$language.name_simple}" loading="lazy">
                      <span class="lang-text">{$language.name_simple}</span>
                    </a>
                  </li>
                {/foreach}
              </ul>
            </li>
          {/if}
          {if isset($currencies) && isset($current_currency)}
            <li class="sub-drop">
              <ul id="abs-currency" class="pop-currency">
                {foreach from=$currencies item=currency}
                  <li {if $currency.current}class="current" {/if}>
                    <a title="{$currency.name}" rel="nofollow" href="{$currency.url}"
                      class="dropdown-item">{$currency.iso_code}</a>
                  </li>
                {/foreach}
              </ul>
            </li>
          {/if}
        </ul>
      </div>
    </div>
    <div class="ets_solo_social_wrapper hover slw_and_alw alw mobile clone">
      <div class="ets_solo_table">
        <div class="ets_solo_tablecell">
          <div class="ets_solo_tablecontent">
            <span class="ets_solo_account_close button" title="">
              <span class="text_close">{l s='Close' d='Shop.Theme.Global'}</span>
            </span>
            <span class="ets_solo_account_close overlay"></span>
            <div class="ets_solo_wrapper_content slw_and_alw alw">
              <h3 class="ets_solo_social_title">{l s='Sign in to your account' d='Shop.Theme.Customeraccount'}</h3>
              <section class="solo-login-form">
                <form id="header-login-form" class="solo-login-form-alw" action="{$urls.pages.authentication}"
                  method="post">
                  <section>
                    <div class="form-group row">
                      <div class="col-md-12">
                        <input class="form-control" name="email" value=""
                          placeholder="{l s='Enter your email...' d='Shop.Theme.Customeraccount'}" required=""
                          type="email">
                      </div>
                    </div>
                    <div class="form-group row">
                      <div class="col-md-12">
                        <input class="form-control js-child-focus js-visible-password"
                          placeholder="{l s='Enter password...' d='Shop.Theme.Customeraccount'}" name="password" value=""
                          pattern=".{literal}{5,}{/literal}" required="" type="password">
                      </div>
                    </div>
                  </section>
                  <footer class="form-footer text-sm-center clearfix">
                    <input type="hidden" name="submitLogin" value="1">
                    <input type="hidden" name="back" value="{$urls.current_url}">
                    <button id="header-submit-login" class="btn btn-primary" data-link-action="sign-in"
                      type="submit">{l s='Sign in' d='Shop.Theme.Actions'}</button>
                    <div class="forgot-password">
                      <a href="{$urls.pages.password}"
                        rel="nofollow">{l s='Forgot your password?' d='Shop.Theme.Customeraccount'}</a>
                    </div>
                    <div class="no-account">
                      <a href="{$urls.pages.register}"
                        data-link-action="display-register-form">{l s='No account? Create here' d='Shop.Theme.Customeraccount'}</a>
                    </div>
                  </footer>
                </form>
              </section>
            </div>
          </div>
        </div>
      </div>
    </div>
  {/if}
</div>