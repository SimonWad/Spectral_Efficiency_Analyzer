def readDataFromFile_PROTOTYPE(self, dataFileName: str):
    # --- Load new file ---
    new_df = readDataFile(os.path.join(ROOT_DIR, dataFileName))

    # Standardize incoming header before processing
    self.df = self.df.copy()  # safety for inplace ops
    self.standardize_header()
    self_header = self.getHeader()

    # Standardize new DF headers
    new_df = new_df.copy()
    temp = OpticalComponentData()
    temp.df = new_df
    temp.standardize_header()
    new_df = temp.df
    new_header = list(new_df.columns)

    # Detect where actual numeric data starts
    start_idx = detect_data_start(new_df)
    new_df = new_df.iloc[start_idx:].reset_index(drop=True)

    # Sort by wavelength column (first column)
    new_df = new_df.sort_values(by=new_header[0])
    new_df.reset_index(drop=True, inplace=True)

    # ------------------------------------------------------------------
    # CASE 1: FIRST FILE → Store as reference spectrum
    # ------------------------------------------------------------------
    if self.df.empty:
        print("→ Initializing reference spectrum")

        # store
        self.df = new_df.copy()
        self.header = new_header

        # Clean: remove NaNs
        self.df.dropna(inplace=True)

        # Normalize intensity
        ycol = self.header[1]
        self.df[ycol] = self.df[ycol] / self.df[ycol].max()

        print("Reference spectrum loaded:")
        print(self.df.head())
        return

    # ------------------------------------------------------------------
    # CASE 2: SUBSEQUENT FILE → Align to reference & append
    # ------------------------------------------------------------------
    print("→ Aligning new file to reference")

    ref = self.df.copy()
    ref_x = ref.iloc[:, 0].values  # reference wavelengths
    ref_header = self.header
    new_x = new_df.iloc[:, 0].values
    new_y = new_df.iloc[:, 1].values

    # ---------------------------------------------------------
    # 1. Clip to shared wavelength domain
    # ---------------------------------------------------------
    xmin = max(ref_x.min(), new_x.min())
    xmax = min(ref_x.max(), new_x.max())

    if xmin >= xmax:
        raise ValueError("No overlapping wavelength range between datasets.")

    # Clip ref_x domain
    mask = (ref_x >= xmin) & (ref_x <= xmax)
    ref_x_clip = ref_x[mask]

    # ---------------------------------------------------------
    # 2. Interpolate new spectrum onto reference wavelength grid
    # ---------------------------------------------------------
    f = interp1d(new_x, new_y, kind="linear", fill_value="extrapolate")
    aligned_y = f(ref_x_clip)

    # Normalize the incoming spectrum
    aligned_y /= np.max(aligned_y)

    # ---------------------------------------------------------
    # 3. Append aligned data as new column
    # ---------------------------------------------------------
    safe_name = f"aligned_{len(self.df.columns)}"
    self.df = self.df.loc[mask].reset_index(drop=True)
    self.df[safe_name] = aligned_y

    print(f"Added aligned dataset: '{safe_name}'")
    print(self.df.head())
