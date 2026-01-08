{**
 * Password recovery page template
 *}
{extends file='page.tpl'}

{block name='page_title'}
  {l s='Nie pamiętasz hasła?' d='Shop.Theme.Customeraccount'}
{/block}

{block name='page_header_container'}
  <header class="page-header">
    {block name='page_title'}
      <h1 class="page-title">{l s='Nie pamiętasz hasła?' d='Shop.Theme.Customeraccount'}</h1>
    {/block}
  </header>
{/block}

{block name='page_content'}
  <form action="{$urls.pages.password}" class="forgotten-password" method="post">

    <ul class="ps-alert-error">
      {foreach $errors as $error}
        <li class="item">
          <i>
            <svg viewBox="0 0 24 24">
              <path fill="#fff" d="M11,15H13V17H11V15M11,7H13V13H11V7M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20Z"></path>
            </svg>
          </i>
          <p>{$error}</p>
        </li>
      {/foreach}
    </ul>

    <header>
      <p class="send-renew-password-link">{l s='Proszę podać adres e-mail użyty podczas rejestracji. Otrzymasz tymczasowy link do zresetowania hasła.' d='Shop.Theme.Customeraccount'}</p>
    </header>

    <div class="card card-login">
      <div class="card-body">
        <div class="form-group">
          <label class="form-control-label required">{l s='Adres e-mail' d='Shop.Forms.Labels'}</label>
          <div class="email">
            <input type="email" name="email" id="email" value="{if isset($smarty.post.email)}{$smarty.post.email|stripslashes}{/if}" class="form-control" required>
          </div>
        </div>
        <footer class="form-footer clearfix">
          <button id="send-reset-link" class="form-control-submit btn btn-primary hidden-xs-down float-xs-right" name="submit" type="submit">
            {l s='Wyślij link do zresetowania' d='Shop.Theme.Actions'}
          </button>
          <button class="form-control-submit btn btn-primary hidden-sm-up float-xs-right" name="submit" type="submit">
            {l s='Wyślij' d='Shop.Theme.Actions'}
          </button>
        </footer>
      </div>
    </div>

  </form>
{/block}

{block name='page_footer'}
  <a href="{$urls.pages.my_account}" class="account-link">
    <i class="material-icons keyboard_arrow_left">&#xE314;</i>
    <span>{l s='Powrót do logowania' d='Shop.Theme.Actions'}</span>
  </a>
{/block}

