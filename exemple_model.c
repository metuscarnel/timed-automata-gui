#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#include "structure_ta.h"


// --------------------- Variables globales ---------------------

char** locations;                 // Locations du TA
DBM** invariants;                   // Invariant de chaque location                     
char** actions;                   // Actions du TA
int* nb_trans_par_location;       // Nombre de transitions sortantes par état
Transition** transitions;        // Transitions sortantes de chaque état
Variable variable;               // Variable de données
UpdateFunction* update_functions; // Fonctions d'update
Constraint* constraints;         // Contraintes

// ---------------------Instantiation TA ---------------------

void init_ta() { //CAN BE OPTIMIZED BY #define NB_LOCATIONS AND NB_ACTIONS, AND HAVING ALL VARIABLES BE ARRAYS
    int nb_locations = 6;
    int nb_actions = 3;

    locations = malloc(nb_locations * sizeof(char*));
    invariants = malloc(nb_locations * sizeof(DBM*));
    actions = malloc(nb_actions * sizeof(char*));
    nb_trans_par_location = malloc(nb_locations * sizeof(int));
    transitions = malloc(nb_locations * sizeof(Transition*));
    update_functions = malloc(nb_actions * sizeof(UpdateFunction));
    constraints = malloc(nb_actions * sizeof(Constraint));

    // Locations
    locations[0] = "l0l3";
    locations[1] = "l0l4";
    locations[2] = "l1l3";
    locations[3] = "l1l4";
    locations[4] = "l2l3";
    locations[5] = "l2l4";
    
    // Invariants
    static DBM i_0 = {{0,0,0},{4,0,infty},{4,infty,0}};
    invariants[0] = &i_0;
    invariants[1] = &i_0;
    invariants[2] = &i_0;
    invariants[3] = &i_0;
    invariants[4] = &i_0;
    invariants[5] = &i_0;


    // Actions
    actions[0] = "a";
    actions[1] = "b";
    actions[2] = "c";

    // Transitions
    nb_trans_par_location[0] = 3;
    transitions[0] = malloc(nb_trans_par_location[0] * sizeof(Transition));
    transitions[0][0] = (Transition){.location_in = 1, .label_action = 2, .guard = {{0,0,-1},{infty,0,infty},{infty,infty,0}}, .reset = {infty,infty}};
    transitions[0][1] = (Transition){.location_in = 2, .label_action = 0, .guard = {{0,-1,0},{infty,0,infty},{infty,infty,0}}, .reset = {infty,infty}};
    transitions[0][2] = (Transition){.location_in = 4, .label_action = 0, .guard = {{0,-2,0},{infty,0,infty},{infty,infty,0}}, .reset = {infty,infty}};    

    nb_trans_par_location[1] = 3;
    transitions[1] = malloc(nb_trans_par_location[1] * sizeof(Transition));
    transitions[1][0] = (Transition){.location_in = 0, .label_action = 1, .guard = {{0,0,-4},{infty,0,infty},{infty,infty,0}}, .reset = {infty,0}};
    transitions[1][1] = (Transition){.location_in = 3, .label_action = 0, .guard = {{0,-1,0},{infty,0,infty},{infty,infty,0}}, .reset = {infty,infty}};
    transitions[1][2] = (Transition){.location_in = 5, .label_action = 0, .guard = {{0,-2,0},{infty,0,infty},{infty,infty,0}}, .reset = {infty,infty}};

    nb_trans_par_location[2] = 2;
    transitions[2] = malloc(nb_trans_par_location[2] * sizeof(Transition));
    transitions[2][0] = (Transition){.location_in = 3, .label_action = 2, .guard = {{0,0,-1},{infty,0,infty},{infty,infty,0}}, .reset = {infty,infty}};
    transitions[2][1] = (Transition){.location_in = 0, .label_action = 2, .guard = {{0,-4,0},{infty,0,infty},{infty,infty,0}}, .reset = {0,infty}};

    nb_trans_par_location[3] = 2;
    transitions[3] = malloc(nb_trans_par_location[3] * sizeof(Transition));
    transitions[3][0] = (Transition){.location_in = 2, .label_action = 1, .guard = {{0,0,-4},{infty,0,infty},{infty,infty,0}}, .reset = {infty,0}};
    transitions[3][1] = (Transition){.location_in = 1, .label_action = 2, .guard = {{0,-4,0},{infty,0,infty},{infty,infty,0}}, .reset = {0,infty}};
    
    nb_trans_par_location[4] = 2;
    transitions[4] = malloc(nb_trans_par_location[4] * sizeof(Transition));
    transitions[4][0] = (Transition){.location_in = 5, .label_action = 2, .guard = {{0,0,-1},{infty,0,infty},{infty,infty,0}}, .reset = {infty,infty}};
    transitions[4][1] = (Transition){.location_in = 0, .label_action = 1, .guard = {{0,-4,0},{infty,0,infty},{infty,infty,0}}, .reset = {0,infty}};

    nb_trans_par_location[5] = 2;
    transitions[5] = malloc(nb_trans_par_location[5] * sizeof(Transition));
    transitions[5][0] = (Transition){.location_in = 4, .label_action = 1, .guard = {{0,0,-4},{infty,0,infty},{infty,infty,0}}, .reset = {infty,0}};
    transitions[5][1] = (Transition){.location_in = 1, .label_action = 1, .guard = {{0,-4,0},{infty,0,infty},{infty,infty,0}}, .reset = {0,infty}};   
}

// --------------------- Initialisation des variables ---------------------

void init_variables() { 
    variable.v = 0;
}

// --------------------- Update functions ---------------------

Variable update_a(Variable var) { if (var.v + 2 <= 10 && var.v + 2 >= -10) var.v += 2; return var; }
Variable update_b(Variable var) { if (var.v - 1 <= 10 && var.v - 1 >= -10) var.v -= 1; return var; }
Variable update_c(Variable var) { if (var.v * 2 <= 10 && var.v * 2 >= -10) var.v *= 2; return var; }

void init_update_functions() {
    update_functions[0] = update_a;
    update_functions[1] = update_b;
    update_functions[2] = update_c;
}

// --------------------- Contraintes ---------------------

bool const_a(Variable var) { return true; }
bool const_b(Variable var) { return true; }
bool const_c(Variable var) { return true; }

void init_constraints() {
    constraints[0] = const_a;
    constraints[1] = const_b;
    constraints[2] = const_c;
}

// --------------------- Remplir la structure TA ---------------------

void fill_ta_struct(TA* ta) {
    init_ta();
    init_variables();
    init_update_functions();
    init_constraints();

    ta->locations = locations;
    ta->invariants = invariants;
    ta->actions = actions;
    ta->nb_trans_par_location = nb_trans_par_location;
    ta->transitions = transitions;
    ta->variable = variable;
    ta->update_functions = update_functions;
    ta->constraints = constraints;
}