{ pkgs ? import <nixpkgs> { } }:
let
  rfRlEnv = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    python = pkgs.python310;
    preferWheels = true;
  };
in
rfRlEnv.env.overrideAttrs (oldAttrs: {
  buildInputs = [ pkgs.geckodriver pkgs.firefox ];
})
