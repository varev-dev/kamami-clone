{block name='login_form'}

  {block name='login_form_errors'}
    {include file='_partials/form-errors.tpl' errors=$errors['']}
  {/block}

  <form id="login-form" action="{block name='login_form_actionurl'}{$action}{/block}" method="post">

    {if isset($back)}
      <input type="hidden" name="back" value="{$back}">
    {/if}

    {block name='login_form_fields'}
      {foreach from=$formFields item="field"}
        {block name='form_field'}
          {if $field.type == 'email'}
            <div class="form-group-w form-group-w-email">
              <div class="form-group row form-group-fr">
                <label class="form-control-label required" for="field-{$field.name}">
                  {$field.label}
                </label>
                <div class="">
                  <input id="field-{$field.name}" class="form-control" name="{$field.name}" type="email" value="{$field.value}"
                    {if $field.autocomplete}autocomplete="{$field.autocomplete}" {/if} {if $field.required}required{/if}>
                </div>
              </div>
              <div class="form-control-comment">
              </div>
            </div>
          {elseif $field.type == 'password'}
            <div class="form-group-w form-group-w-password">
              <div class="form-group row form-group-fr">
                <label class="form-control-label required" for="field-{$field.name}">
                  {$field.label}
                </label>
                <div class="">
                  <div class="input-group js-parent-focus">
                    <input id="field-{$field.name}" class="form-control js-child-focus js-visible-password" name="{$field.name}"
                      title="{l s='Co najmniej 5 znaków' d='Shop.Forms.Help'}"
                      aria-label="{l s='Hasło musi zawierać przynajmniej 5 znaków' d='Shop.Forms.Help'}" type="password"
                      {if $field.autocomplete}autocomplete="{$field.autocomplete}" {/if} value=""
                      pattern=".{literal}{{/literal}5,{literal}}{/literal}" {if $field.required}required{/if}>
                    <span class="input-group-btn show-password">
                      <button class="btn" type="button" data-action="show-password"
                        data-text-show="{l s='Pokaż' d='Shop.Theme.Actions'}"
                        data-text-hide="{l s='Ukryj' d='Shop.Theme.Actions'}">
                        {l s='Pokaż' d='Shop.Theme.Actions'}
                      </button>
                    </span>
                  </div>
                </div>
              </div>
              <div class="form-control-comment">
              </div>
            </div>
          {else}
            {form_field field=$field}
          {/if}
        {/block}
      {/foreach}
    {/block}

    {block name='login_form_footer'}
      <footer class="form-footer text-sm-center clearfix">
        <input type="hidden" name="submitLogin" value="1">
        {block name='form_buttons'}
          <button id="submit-login" class="btn btn-primary" data-link-action="sign-in" type="submit">
            {l s='Zaloguj się' d='Shop.Theme.Actions'}
          </button>
        {/block}
      </footer>
    {/block}

  </form>
{/block}