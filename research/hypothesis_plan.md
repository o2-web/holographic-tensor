# Перспективные ветви развития и план проверки гипотез

Этот документ переводит идею holographic tensor compression в набор конкретных, проверяемых исследовательских ветвей. Цель — не считать представление полезным по умолчанию, а найти режимы данных, где оно выигрывает, проигрывает или требует отдельного варианта кодирования.

## Контекст

Текущий метод — точное обратимое кодирование:

```text
A(x, y, z) -> (I(x, y), V_i(z))
```

Метод наиболее перспективен, когда многие позиции `(x, y)` разделяют одинаковые или почти одинаковые z-векторы. В таких режимах 3D-тензор можно представить как 2D-карту индексов плюс меньшую таблицу базовых z-векторов. Центральный вопрос: не только обратимо ли преобразование, а дает ли эта структурная декомпозиция измеримый выигрыш относительно честных baseline-методов с одинаковой сериализацией.

---

## Перспективные ветви развития

### Ветвь A — Lossless structural compression

**Идея:** Сохранить текущую точную dictionary-based схему, но сделать ее количественно измеримой и сопоставимой с baseline-компрессорами.

**Почему перспективно:** Метод должен хорошо работать на тензорах с повторяющимися срезами, блочной структурой, периодическими паттернами, категориальными объемами, повторяющимися состояниями симуляций, voxel-labels и дискретизированными научными полями.

**Главный риск:** Для высокоэнтропийных тензоров с почти уникальными z-векторами таблица и карта индексов могут добавить overhead относительно raw storage или general-purpose compression.

### Ветвь B — Sparse-aware holographic encoding

**Идея:** Добавить sparse-представление для z-векторов и/или index map, когда тензор содержит много нулей или мало активных событий.

**Почему перспективно:** Sparse-тензоры часто встречаются в event volumes, masks, occupancy grids и научных измерениях. Комбинация sparse-координат и дедупликации векторов может быть сильнее каждого подхода отдельно.

**Главный риск:** Sparse-метаданные могут съесть выигрыш, если тензор только умеренно разрежен.

### Ветвь C — Approximate / lossy basis matching

**Идея:** Разрешить похожим z-векторам разделять одну запись таблицы при контролируемом пороге расстояния или квантовании.

**Почему перспективно:** В реальных float-тензорах часто есть шумные варианты небольшого числа латентных профилей. Approximate matching может дать большой выигрыш там, где точная дедупликация не срабатывает.

**Главный риск:** Lossy-режим меняет claim проекта с точной обратимости на rate-distortion tradeoff, поэтому он должен быть отделен от lossless API и оцениваться явными метриками ошибки.

### Ветвь D — Hierarchical and block-local dictionaries

**Идея:** Разбить плоскость `(x, y)` на tiles и строить локальные таблицы векторов на tile, опционально с global fallback table.

**Почему перспективно:** Локальные словари могут использовать spatial locality, когда паттерны повторяются внутри регионов, но не глобально. Это может снизить энтропию индексов и улучшить cache behavior.

**Главный риск:** Слишком много локальных таблиц увеличит metadata overhead и ухудшит compression ratio.

### Ветвь E — Index-surface entropy coding

**Идея:** Рассматривать `I(x, y)` как image-like surface и сжимать ее через run-length, delta, block или entropy coding.

**Почему перспективно:** Если соседние позиции `(x, y)` часто ссылаются на один z-вектор, сама карта индексов должна хорошо сжиматься.

**Главный риск:** Если распределение индексов шумное или случайное, специализированное surface coding может не превзойти gzip/zstd на простой сериализации.

### Ветвь F — Domain-specific benchmark kits

**Идея:** Собрать synthetic и real-data benchmark suites для доменов, где повторяющиеся z-профили правдоподобны.

**Почему перспективно:** Концепции нужны доказательства в конкретных доменах, а не только на generic random tensors.

**Кандидаты доменов:** voxel labels, medical segmentation masks, geospatial raster stacks, simulation volumes, embedding grids, temporal sensor arrays и cellular automata state histories.

**Главный риск:** Предобработка доменных данных может неявно подыгрывать методу; протокол должен явно фиксировать такие допущения.

---

## Проверяемые гипотезы

Первые executable checks для H1 добавлены в `tests/test_hypothesis_testing.py`: они сравнивают high-redundancy tensor с negative-control tensor, где каждый z-вектор уникален.

| ID | Гипотеза | Критерий успеха | Сигнал опровержения |
| --- | --- | --- | --- |
| H1 | Точная дедупликация z-векторов выигрывает на high-redundancy tensors. | Compression ratio минимум в 1.5 раза лучше raw storage и не хуже gzip/zstd более чем на 10% на repeated-profile data. | General compressors стабильно равны или лучше при меньшей latency. |
| H2 | У метода есть предсказуемая break-even zone, зависящая от table cardinality. | Простая модель предсказывает helpful vs harmful regimes по `|V|/(X*Y)`, `Z` и index entropy. | Результаты остаются шумными после контроля этих переменных. |
| H3 | Sparse-aware encoding улучшает event-like tensors. | Hybrid sparse/dictionary mode улучшает ratio минимум на 20% относительно dense dictionary mode при высокой sparsity. | Sparse metadata уничтожает выигрыш на большинстве уровней sparsity. |
| H4 | Approximate matching открывает выигрыш для noisy profile families. | Lossy mode дает лучшую rate-distortion curve, чем exact mode плюс general compression. | Ошибка квантования растет быстрее, чем улучшается compression. |
| H5 | Index-surface coding полезен при spatially coherent index maps. | Surface-coded indexes уменьшают encoded index bytes минимум на 25% на block/periodic datasets. | gzip/zstd на raw index map стабильно не хуже. |
| H6 | Local dictionaries улучшают spatially heterogeneous tensors. | Tile-local dictionaries выигрывают у global dictionary на данных с region-specific profile reuse. | Metadata overhead перевешивает локальный reuse. |

---

## План проверки гипотез

### Stage 0 — Experimental contract

**Цель:** Сделать каждый результат воспроизводимым и сравнимым.

**Задачи:**
1. Зафиксировать одну canonical binary serialization для raw tensors, compressed index maps и vector tables.
2. Записывать environment metadata: Python version, NumPy version, CPU model, OS и git commit.
3. Использовать фиксированные random seeds для synthetic data families.
4. Сохранять каждый run как structured JSON/CSV с config, metrics и timing summary.

**Exit criteria:** Одна команда регенерирует baseline results из committed configs.

### Stage 1 — Baseline lossless benchmark

**Покрывает гипотезы:** H1, H2.

**Datasets:**
- iid random integer tensors как negative control;
- repeated-profile tensors с контролируемой table cardinality;
- block-structured tensors;
- periodic/wave profile tensors.

**Metrics:**
- raw bytes;
- compressed bytes;
- gzip/zstd bytes на тех же serialized inputs;
- encode/decode latency;
- peak memory;
- `|V|`, `|V|/(X*Y)` и index entropy.

**Decision rule:** Продолжать lossless-ветку только если есть четкий winning regime и измеримая break-even boundary.

### Stage 2 — Phase diagram and break-even model

**Покрывает гипотезы:** H2.

**Experiment grid:** Sweep по `X`, `Y`, `Z`, table cardinality, spatial coherence, value dtype и randomness seed.

**Analysis:**
- обучить простые predictive models для compression ratio и runtime;
- построить helpful/neutral/harmful regions;
- определить минимальный набор метрик, предсказывающих выигрыш.

**Decision rule:** Если break-even model интерпретируема и стабильна, использовать ее для automatic encoder selection.

### Stage 3 — Sparse-aware prototype

**Покрывает гипотезы:** H3.

**Implementation variants:**
- текущий dense method;
- sparse z-vector table entries;
- sparse index map для dominant background vectors;
- hybrid mode с threshold-based selection.

**Datasets:** Sparse-event tensors с controlled event density, clustered events и random events.

**Decision rule:** Оставлять sparse mode только если он выигрывает в документированном диапазоне sparsity и автоматически откатывается вне этого диапазона.

### Stage 4 — Approximate matching prototype

**Покрывает гипотезы:** H4.

**Implementation variants:**
- quantized z-vectors;
- distance-threshold matching;
- centroid/prototype table with reconstruction.

**Metrics:**
- compressed bytes;
- mean absolute error;
- max error;
- domain-specific error при добавлении real dataset;
- encode/decode latency.

**Decision rule:** Оставлять lossy mode только как отдельный API с явным error reporting и rate-distortion curve, которая превосходит simple quantization плюс gzip/zstd.

### Stage 5 — Index-surface and local dictionary variants

**Покрывает гипотезы:** H5, H6.

**Implementation variants:**
- run-length encoding для index rows;
- block coding для index tiles;
- entropy coding of index streams;
- global dictionary vs tile-local dictionaries vs hybrid fallback.

**Datasets:** Spatially coherent blocks, noisy blocks, periodic surfaces и heterogeneous regions.

**Decision rule:** Оставлять варианты, улучшающие Pareto frontier compression ratio vs latency без чрезмерной сложности.

### Stage 6 — Domain validation

**Покрывает гипотезы:** H1-H6 в зависимости от домена.

**Candidate datasets:**
- segmentation/label volumes;
- geospatial raster time stacks;
- simulation snapshots;
- occupancy grids;
- temporal sensor grids.

**Protocol:**
1. Документировать preprocessing.
2. Запускать raw, general-compressor, exact, sparse, lossy и index-coded variants.
3. Отчетно показывать, где каждый encoder выигрывает и проигрывает.

**Decision rule:** Ветвь становится серьезным research direction только если выигрывает хотя бы на одном realistic domain dataset при прозрачном протоколе.

---

## План первых 30 дней

### Week 1 — Benchmark skeleton
- Добавить `experiments/` с configs, scripts и results placeholders.
- Реализовать canonical serializers.
- Сгенерировать synthetic repeated-profile, random, block и sparse tensors.
- Выводить JSON metrics для одного run.

### Week 2 — Baseline comparison
- Добавить сравнение с gzip и zstd/lz4, если dependencies доступны.
- Прогнать grid по sizes и redundancy levels.
- Получить первые ratio и latency tables.

### Week 3 — Analysis notebook or script
- Посчитать index entropy и table-cardinality metrics.
- Построить compression ratio vs `|V|/(X*Y)` and `Z`.
- Черновик первой break-even phase diagram.

### Week 4 — Go / no-go review
- Решить, какие ветви продолжать:
  - продолжать exact lossless, если H1/H2 поддержаны;
  - начать sparse prototype, если sparse datasets показывают overhead у dense mode;
  - начать lossy prototype только если noisy-profile data ломает exact matching, но сохраняет низкую reconstruction error при quantization.
- Превратить winning branches в implementation tickets с acceptance criteria.

---

## Рекомендуемый приоритет

1. **Lossless structural compression + fair baselines** — фундамент для всех остальных ветвей.
2. **Break-even modeling** — показывает пользователям, когда метод не надо использовать.
3. **Index-surface coding** — вероятно low-complexity improvement, потому что представление уже порождает 2D surface.
4. **Sparse-aware mode** — перспективно для event и occupancy tensors.
5. **Approximate matching** — высокий потенциал, но нужен отдельный режим, потому что меняется claim об обратимости.
6. **Domain benchmark kits** — необходимы перед сильными практическими заявлениями.
