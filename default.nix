# Not editable because this is only used during training, not development.

{ pkgs ? import <nixpkgs> { } }:
pkgs.poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  buildInputs = [ pkgs.geckodriver ];
}
