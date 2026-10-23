use anchor_lang::prelude::*;
use solana_program::{pubkey::Pubkey, system_instruction, sysvar};
use anchor_spl::token::{self, Token, TokenAccount};


declare_id!("YourProgramIDHere");

#[program]
pub mod my_token_project {
    use super::*;
    
    pub fn initialize(ctx: Context<Initialize>, mint_authority: Pubkey, decimals: u8) -> ProgramResult {
        // Initialize the mint for the token
        token::mint_to(
            ctx.accounts.into(),
            mint_authority,
            decimals,
        )?;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = user, space = 8 + 82)]
    pub mint: Account<'info, token::Mint>,
    
    #[account(mut)]
    pub user: Signer<'info>,
    
    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
}
