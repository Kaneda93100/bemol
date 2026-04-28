
import bemol

"""Test definition of secondary effects."""
dummy_rotor = bemol.rotor.mexico
# model = bemol.bem.BaseBEM(dummy_rotor,corrections={})
model = bemol.bem.BaseBEM(
    dummy_rotor,
    corrections=[
        bemol.secondary.hubTipLoss.Prandtl,
        bemol.secondary.skewAngle.Burton
        ])