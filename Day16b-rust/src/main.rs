use std::collections::HashSet;
use std::fs::read_to_string;
use petgraph::graphmap::{UnGraphMap};
use petgraph::algo::{dijkstra};
use std::time::Instant;

fn read_racetrack() -> (Vec<String>, [i64; 2], [i64; 2]){
    let mut racetrack:Vec<String> = Vec::new();
    let mut start = [1i64; 2];
    let mut end = [1i64; 2];
    for l in read_to_string("input.txt").unwrap().lines() {
        let mut line:String = l.parse().unwrap();

        let end_x = line.find("E");
        if end_x != None {
            end = [racetrack.len() as i64, end_x.unwrap() as i64];
            line = line.replace("E", ".");
        }

        let start_x = line.find("S");
        if start_x != None {
            start = [racetrack.len() as i64, start_x.unwrap() as i64];
            line = line.replace("S", ".");
        }

        racetrack.push(line);
    }

    (racetrack, start, end)
}

#[inline(always)]
fn reverse_dir(dir:[i64; 2]) -> [i64; 2] {
    return if dir[0] == 1 {
        [-1, 0]
    } else if dir[0] == -1 {
        [1, 0]
    } else if dir[1] == 1 {
        [0, -1]
    } else {
        [0, 1]
    }
}

#[inline(always)]
fn add_dir(coord:[i64; 2], dir:[i64; 2]) ->[i64; 2] {
    [coord[0]+dir[0], coord[1]+dir[1]]
}

fn populate_graph(racetrack:Vec<String>, end:[i64; 2]) -> UnGraphMap<([i64; 2], [i64; 2]), u64> {
    //let mut rt = GraphMap::<((i64, i64), (i64, i64)), ()>::new();
    let mut rt:UnGraphMap<([i64; 2], [i64; 2]), u64> = UnGraphMap::with_capacity(20125, 30000);

    let all_dirs = [
        [0, -1],
        [0, 1],
        [1, 0],
        [-1, 0]
    ];

    //let mut edges:HashSet<(([i64; 2], [i64; 2]), ([i64; 2], [i64; 2]), u64)> = HashSet::new();
    for (y, line) in racetrack.iter().enumerate() {
        for (x, char) in line.chars().enumerate() {
            if char == '.' {
                let space = [y as i64, x as i64];
                for facing in all_dirs {
                    for new_facing in all_dirs{
                        if new_facing == reverse_dir(facing) {
                            continue
                        }

                        let adj = add_dir(space, new_facing);
                        let adj_char = racetrack[y].chars().nth(x).unwrap();
                        if adj_char == '.' {
                            if facing == new_facing {
                                rt.add_edge((space, facing), (adj, facing), 1);
                                //edges.insert(((space, facing), (adj, facing), 1));
                            }
                            else {
                                rt.add_edge((space, facing), (adj, new_facing), 1001);
                                //edges.insert(((space, facing), (adj, new_facing), 1001));
                            }
                        }
                    }
                }
            }
        }
    }

    for facing in all_dirs {
        rt.add_edge((end, facing), (end, [0,0]), 0);
        //edges.insert(((end, facing), (end, [0,0]), 0));
    }

    rt
}

fn main() {
    let start_time = Instant::now();

    let (racetrack, start, end) = read_racetrack();
    let rt = populate_graph(racetrack, end);

    let paths_from_start = dijkstra(&rt, (start, [0, 1]), None, |(_a, _b, weight)| *weight);
    let minimum_length = paths_from_start[&(end, [0, 0])];
    let paths_from_end = dijkstra(&rt, (end, [0, 1]), None, |(_a, _b, weight)| *weight);

    let mut cords_on_shortest_path = HashSet::new();
    for ((cord, dir), cost_from_start) in paths_from_start.into_iter() {
        if cost_from_start < minimum_length {
            let cost_from_end = paths_from_end[&(cord, dir)];
            if (cost_from_start + cost_from_end) == minimum_length{
                cords_on_shortest_path.insert(cord);
            }
        }
    }

    let end_time = Instant::now();
    let duration = (end_time - start_time).as_micros();

    println!("Minimum length {:?}", minimum_length);
    println!("Cords on shortest: {:?}", cords_on_shortest_path.len()+1);
    println!("Elapsed time {:?}μs", duration);
}
