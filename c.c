#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    // Check if at least one argument is provided
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <args>\n", argv[0]);
        return 1;
    }

    // Prepare the argument list for execvp
    char *args[argc + 2]; // +2 for "python" and "main.py"
    args[0] = "python";    // Python interpreter
    args[1] = "main.py";   // Python script to execute

    // Copy the arguments passed to the binary
    for (int i = 1; i < argc; i++) {
        args[i + 1] = argv[i];
    }
    args[argc + 1] = NULL; // Null-terminate the argument list

    // Execute the Python script
    execvp(args[0], args);

    // If execvp fails
    perror("execvp failed");
    return 1;
}
