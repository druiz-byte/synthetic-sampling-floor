# Monte Carlo checks of Sect. 3

- Eq. (5), p = 0.5, n_r = 789, n_s = 1000: closed form 4.67 pp · Monte Carlo 4.66 pp
- Eq. (5), p = 0.3, n_r = 789, n_s = 500: closed form 5.13 pp · Monte Carlo 5.13 pp
- Eq. (5), p = 0.1, n_r = 789, n_s = 2000: closed form 2.47 pp · Monte Carlo 2.47 pp
- Eq. (3), k = 4, n_s = 1000: closed form 3.13 · Monte Carlo 3.12 TV points
- Eq. (3), k = 5, n_s = 500: closed form 4.56 · Monte Carlo 4.55 TV points
- Eq. (3), k = 6, n_s = 2000: closed form 3.00 · Monte Carlo 3.00 TV points

| n_s | P(pass), unbiased | P(pass), bias 2 pp | P(pass), bias 4 pp |
|---|---|---|---|
| 250 | 0.950 | 0.914 | 0.804 |
| 500 | 0.950 | 0.892 | 0.713 |
| 1,000 | 0.951 | 0.868 | 0.609 |
| 2,000 | 0.950 | 0.842 | 0.522 |
| 10,000 | 0.950 | 0.808 | 0.420 |