# Release Checklist

## Pre-Release Checks
- [ ] **Changelog**: Ensure `CHANGELOG.md` is updated with the new version (vX.Y.Z) and release notes.
- [ ] **Manifest**: Verify `manifest.json` version matches the tag (SemVer).
- [ ] **Validation**: Run local checks:
  - `ruff format custom_components/oblamatik`
  - `ruff check custom_components/oblamatik`
  - `mypy custom_components/oblamatik`
- [ ] **Git Tag**: Create and push the tag:
  ```bash
  git tag vX.Y.Z
  git push origin vX.Y.Z
  ```

## Post-Release Verification (HACS)
After the GitHub Action `release.yml` completes:

1.  **HACS Update**:
    -   Go to HACS -> Integrations -> Oblamatik.
    -   Click the three dots -> **Redownload**.
    -   (Optional if issues occur) **Clear downloads** -> **Reinstall**.
2.  **Restart**: Restart Home Assistant.
3.  **Verify**:
    -   [ ] Check if entities load correctly.
    -   [ ] Verify no new errors in Home Assistant logs related to `oblamatik`.
    -   [ ] Test basic functionality (e.g., toggle a switch).

## Assets Check
- [ ] Confirm `oblamatik.zip` is attached to the GitHub Release.
