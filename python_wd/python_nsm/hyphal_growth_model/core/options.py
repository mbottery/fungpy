# core/options.py

from dataclasses import dataclass, field

@dataclass
class Options:
    
    # Core simulation parameters
    growth_rate: float = 1.0
    time_step: float = 1.0

    # Branching behaviour
    branch_probability: float = 0.4                 # ⬅️ Was 0.1 in Python
    max_branches: int = 8                           # ⬅️ Java default
    branch_angle_spread: float = 180.0              # ⬅️ Java GUI
    field_threshold: float = 0.06                   # ⬅️ Branch if field < value
    branch_time_window: float = 40.0
    branch_sensitivity: float = 1.0
    optimise_initial_branching: bool = True
    leading_branch_prob: float = 0.0
    allow_internal_branching: bool = True           # ⬅️ Enabled in Java GUI

    # Tropisms
    autotropism: float = 1.0
    gravitropism: float = 0.0
    random_walk: float = 0.2
    length_scaled_growth: bool = True
    length_growth_coef: float = 0.1
    curvature_branch_bias: float = 0.25 # How much the recent path curvature biases branching
    
    # Directional memory (EMA decay)
    direction_memory_blend: float = 0.2  # 0.0 = ignore history, 1.0 = no smoothing
    field_alignment_boost: float = 0.2  # Boost growth if aligned with field gradient
    field_curvature_influence: float = 0.2

    # Age & Length limitations
    max_length: float = 50.0                        # ⬅️ Java sets 50.0
    max_age: float = 300.0                          # ⬅️ Java age limit
    min_tip_age: float = 10.0
    min_tip_length: float = 10.0
    die_if_old: bool = False
    die_if_too_dense: bool = True
    min_supported_tips: int = 16
    max_supported_tips: int = 1000                    # ⬅️ Java GUI

    # Density field
    density_field_enabled: bool = True
    density_threshold: float = 0.2
    charge_unit_length: float = 20.0
    neighbour_radius: float = 20.0
    density_from_tips: bool = True
    density_from_branches: bool = True
    density_from_all: bool = True                   # ⬅️ Java GUI marks "all mycelia"

    # Gravitropism curvature (angle-based)
    gravi_angle_start: float = 100.0
    gravi_angle_end: float = 500.0
    gravi_angle_max: float = 180.0
    gravi_layer_thickness: float = 40.0

    # Data & debugging
    record_dead_tips: bool = True
    source_config_path: str = ""

    # Nutrient field settings
    use_nutrient_field: bool = False
      
    # Legacy-style attractors/repellents (for advanced use or CLI setup)
    nutrient_attractors: list = field(default_factory=lambda: [((30, 30, 0), 1.0)])  # (pos3D, strength)
    nutrient_repellents: list = field(default_factory=lambda: [((-20, -20, 0), -1.0)])
      
    # GUI-friendly default single field (with user inputs)
    nutrient_attraction: float = 0.0                 # overall attractor strength
    nutrient_repulsion: float = 0.0                  # overall repellent strength
    nutrient_attract_pos: str = "30,30,0"            # attractor coordinates (comma string for GUI)
    nutrient_repel_pos: str = "-20,-20,0"            # repellent coordinates
    nutrient_radius: float = 50.0                    # range of influence
    nutrient_decay: float = 0.05                     # falloff rate

    # In core/options.py
    anisotropy_enabled: bool = False
    anisotropy_vector: tuple = (1.0, 0.0, 0.0)  # Bias along +X by default
    anisotropy_strength: float = 0.1            # How much influence to apply
    
    # Reproducibility
    seed: int = 123
