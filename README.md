[//]: # (STANDARD README)
[//]: # (https://github.com/RichardLitt/standard-readme)
[//]: # (----------------------------------------------)
[//]: # (Uncomment optional sections as required)
[//]: # (----------------------------------------------)

[//]: # (Title)
[//]: # (Match repository name)
[//]: # (REQUIRED)

# tocgen

[//]: # (Banner)
[//]: # (OPTIONAL)
[//]: # (Must not have its own title)
[//]: # (Must link to local image in current repository)


[//]: # (Badges)
[//]: # (OPTIONAL)
[//]: # (Must not have its own title)


[//]: # (Short description)
[//]: # (REQUIRED)
[//]: # (An overview of the intentions of this repo)
[//]: # (Must not have its own title)
[//]: # (Must be less than 120 characters)
[//]: # (Must match GitHub's description)

Generate Table of Contents for Markdown files

[//]: # (Long Description)
[//]: # (OPTIONAL)
[//]: # (Must not have its own title)
[//]: # (A detailed description of the repo)

Automatic Markdown Table of Contents generator with YAML configuration and CI support.

## Table of Contents

[//]: # (REQUIRED)
[//]: # (Managed automatically)
[//]: # (Changes between the TABLE_OF_CONTENTS_START and TABLE_OF_CONTENTS_END markers will be overritten)

[//]: # (TOCGEN_TABLE_OF_CONTENTS_START)

[//]: # (Table of contents will be automatically generated and inserted here.)

[//]: # (TOCGEN_TABLE_OF_CONTENTS_END)

[//]: # (## Security)
[//]: # (OPTIONAL)
[//]: # (May go here if it is important to highlight security concerns.)



[//]: # (## Background)
[//]: # (OPTIONAL)
[//]: # (Explain the motivation and abstract dependencies for this repo)

## Install

[//]: # (Explain how to install the thing.)
[//]: # (OPTIONAL IF documentation repo)
[//]: # (ELSE REQUIRED)

Just run the requirements:

`pip3 install -r requirements.txt`

## Usage
[//]: # (REQUIRED)
[//]: # (Explain what the thing does. Use screenshots and/or videos.)

### Example

You might have a README.md that looks a bit like this

```markdown
# repo-name

## Install

Lorem ipsum dolor sit amet.
 
## Usage

Consectetur adipiscing elit.
 ```

It is often a good idea to include a Table of Contents at the top to aid readability, something that is recommended by
standard readme. Updating this becomes a pain whenever you add a new heading though. Instead, just add the tocgen
markers.

```markdown
# repo-name

## Table of Contents

[//]: # (TOCGEN_TABLE_OF_CONTENTS_START)

[//]: # (Table of contents will be automatically generated and inserted here.)

[//]: # (TOCGEN_TABLE_OF_CONTENTS_END)

## Install

Lorem ipsum dolor sit amet.
 
## Usage

Consectetur adipiscing elit.
```

Now, tocgen takes ownership of everything between TOCGEN_TABLE_OF_CONTENTS_START and TOCGEN_TABLE_OF_CONTENTS_END, so
every time you change the headings, your table of contents updates automatically.


[//]: # (Extra sections)
[//]: # (OPTIONAL)
[//]: # (This should not be called "Extra Sections".)
[//]: # (This is a space for ≥0 sections to be included,)
[//]: # (each of which must have their own titles.)

## Configuration


### CLI Args
Config can be passed as CLI args

`python3 tocgen.py [flags]`

### YAML Configuration

If the declarative life is more your speed, add a `.tocgen.yml` file to the root of your repo and set your config as
appropriate. See below.

### Configuration Reference

| CLI Flag       | YAML Variable      | Type    | Default                               | Permitted Values                                               | Description                                                                                       |
|----------------|--------------------|---------|---------------------------------------|----------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `--files`      | `files`            | list    | *None*                                | Any valid file path(s)                                         | List of Markdown files to update. If omitted, all `.md` files containing TOC markers are scanned. |
| `--config`     | *(not applicable)* | string  | `.tocgen.yml` or `.github/tocgen.yml` | Valid file path                                                | Path to a YAML config file. Loaded automatically if found.                                        |
| `--start`      | `start`            | string  | `TOCGEN_TABLE_OF_CONTENTS_START`      | Any string                                                     | Marker identifying where the TOC should begin. Must appear in the file.                           |
| `--end`        | `end`              | string  | `TOCGEN_TABLE_OF_CONTENTS_END`        | Any string                                                     | Marker identifying where the TOC should end. Must appear in the file.                             |
| `--indent`     | `indent`           | integer | `4`                                   | Any positive integer                                           | Number of spaces used to indent sub-headings in the TOC.                                          |
| `--min-level`  | `min_level`        | integer | `2`                                   | 1, 2, 3, 4, 5, 6                                               | Minimum heading level to include (e.g. `2` to skip document titles).                              |
| `--max-level`  | `max_level`        | integer | `6`                                   | 1, 2, 3, 4, 5, 6                                               | Maximum heading level to include.                                                                 |
| `--list-style` | `list_style`       | string  | `ordered`                             | `ordered`, `unordered`, `number`, `bullet`, `o`, `n`, `u`, `b` | Determines list style for the TOC.                                                                |

### Precedence

CLI flags override YAML variables, which override built-in defaults.  

### Markers

Can appear in Markdown (`[//]: # (TAG)`) or HTML (`<!-- TAG -->`) comment form — `tocgen` searches only for the marker text itself.  

### Automatic discovery

If neither `--files` nor `files:` is provided, all Markdown files containing both start and end markers are processed.

## Use of Headings for Accessibility

In Markdown, a level 1 heading (`# Heading`) is intended to represent the **document title**, not just "large text".
Using multiple level 1 headings within the same file can confuse screen readers and accessibility tools that rely on a
clear heading hierarchy. For best results, use a single top-level heading for the document title and begin your content
structure with level 2 (`##`) or lower. This ensures consistent navigation for assistive technologies and improves
overall readability.

## Documentation

Further documentation is in the [`docs`](docs/) directory.

## Repository Configuration

> [!WARNING]  
> This repo is controlled by OpenTofu in the [estate-repos](https://github.com/evoteum/estate-repos) repository.  
>  
> Manual configuration changes will be overwritten the next time OpenTofu runs.


[//]: # (## API)
[//]: # (OPTIONAL)
[//]: # (Describe exported functions and objects)



[//]: # (## Maintainers)
[//]: # (OPTIONAL)
[//]: # (List maintainers for this repository)
[//]: # (along with one way of contacting them - GitHub link or email.)



[//]: # (## Thanks)
[//]: # (OPTIONAL)
[//]: # (State anyone or anything that significantly)
[//]: # (helped with the development of this project)



## Contributing
[//]: # (REQUIRED)
If you need any help, please log an issue and one of our team will get back to you.

PRs are welcome.


## License
[//]: # (REQUIRED)

### Code

All source code in this repository is licenced under the [GNU Affero General Public License v3.0 (AGPL-3.0)](https://www.gnu.org/licenses/agpl-3.0.en.html). A copy of this is provided in the [LICENSE](LICENSE).

### Non-code content

All non-code content in this repository, including but not limited to images, diagrams or prose documentation, is licenced under the [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/) licence.
