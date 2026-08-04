# Vehicle Coverage Matrix (Version 1)

## Dataset Registry

Each vehicle receives a permanent Dataset ID used for ETL, validation,
testing and future version tracking.

  Dataset ID   Brand           Model            Segment
  ------------ --------------- ---------------- --------------------
  V001         Maruti Suzuki   Alto K10         Entry Hatchback
  V002         Maruti Suzuki   S-Presso         Entry Hatchback
  V003         Renault         Kwid             Entry Hatchback
  V004         Maruti Suzuki   Swift            Hatchback
  V005         Hyundai         Grand i10 Nios   Hatchback
  V006         Tata            Tiago            Hatchback
  V007         Maruti Suzuki   Baleno           Premium Hatchback
  V008         Hyundai         i20              Premium Hatchback
  V009         Tata            Altroz           Premium Hatchback
  V010         Maruti Suzuki   Dzire            Compact Sedan
  V011         Honda           Amaze            Compact Sedan
  V012         Hyundai         Aura             Compact Sedan
  V013         Maruti Suzuki   Ciaz             Mid-size Sedan
  V014         Honda           City             Mid-size Sedan
  V015         Hyundai         Verna            Mid-size Sedan
  V016         Volkswagen      Virtus           Mid-size Sedan
  V017         Skoda           Slavia           Mid-size Sedan
  V018         Maruti Suzuki   Fronx            Micro SUV
  V019         Tata            Punch            Micro SUV
  V020         Hyundai         Exter            Micro SUV
  V021         Maruti Suzuki   Brezza           Compact SUV
  V022         Tata            Nexon            Compact SUV
  V023         Hyundai         Venue            Compact SUV
  V024         Kia             Sonet            Compact SUV
  V025         Mahindra        XUV 3XO          Compact SUV
  V026         Maruti Suzuki   Grand Vitara     Mid-size SUV
  V027         Hyundai         Creta            Mid-size SUV
  V028         Kia             Seltos           Mid-size SUV
  V029         Toyota          Hyryder          Mid-size SUV
  V030         Honda           Elevate          Mid-size SUV
  V031         MG              Astor            Mid-size SUV
  V032         Volkswagen      Taigun           Mid-size SUV
  V033         Skoda           Kushaq           Mid-size SUV
  V034         Maruti Suzuki   Ertiga           MPV
  V035         Maruti Suzuki   XL6              MPV
  V036         Kia             Carens           MPV
  V037         Toyota          Rumion           MPV
  V038         Maruti Suzuki   Invicto          Premium MPV
  V039         Toyota          Innova Hycross   Premium MPV
  V040         Maruti Suzuki   e Vitara         Electric SUV
  V041         Tata            Tiago EV         Electric Hatchback
  V042         MG              Comet EV         Electric Hatchback
  V043         Tata            Curvv EV         Electric SUV
  V044         Tata            Nexon EV         Electric SUV
  V045         Mahindra        BE 6             Electric SUV
  V046         MG              Windsor EV       Electric SUV
  V047         Hyundai         Creta Electric   Electric SUV

## Notes

-   Dataset IDs are immutable once assigned.
-   New vehicles should continue sequential numbering (e.g. V048,
    V049...).
-   The Dataset ID is independent of variant selection and can be reused
    across future dataset versions.

## Next Deliverable

Populate `sample-vehicles.csv` using these Dataset IDs and the canonical
master vehicle template. Begin with one representative variant per model
and progressively enrich the dataset with specifications.
