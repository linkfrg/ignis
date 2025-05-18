CAVA_CDEF = """
void cava_execute(double *cava_in, int new_samples, double *cava_out, struct cava_plan *plan);

void* cava_init(int bars, int sample_rate, int stereo, int framerate,
                float gravity, int integral, int monstercat);

void cava_destroy(struct cava_plan *plan);
"""
