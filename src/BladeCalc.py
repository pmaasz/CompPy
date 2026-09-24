import math
from math import atan, cos, sin, pi, radians
import stl


################################
##Function: NACA4Blade
##Inputs:
#camberRoot: camber of root (float)
#camberTip: camber of tip (float)
#camberPos: posistion of maximum camber (float)
#thickness: maximum thickness (float)
#bladeHeight: blade height (float)
#twistAngle: blade twist (float)
#rootChord: chord at root (float)
#tipChord: chord at tip (float)
#cot: center of twist coordinates (list)
##Returns:
#(faces, verts): list of faces and list of verts
################################
def NACA4Blade(camberRoot, camberTip, camberPos, thickness,
                        bladeHeight, twistAngle, rootChord, tipChord, cot):
    if bladeHeight <= 0:
        raise ValueError("bladeHeight must be > 0")
    if rootChord <= 0 or tipChord <= 0:
        raise ValueError("rootChord and tipChord must be > 0")
    if not 0.0 < camberPos < 1.0:
        raise ValueError("camberPos must be in (0, 1)")
    if len(cot) != 2:
        raise ValueError("cot must have 2 coordinates")

    twist = radians(twistAngle) / bladeHeight

    cot = [x / 100 for x in cot]

    nspan = 1
    # Number of points per surface, INCLUDING the trailing edge.
    # Previously only npts points were emitted while npts+1 were computed,
    # silently dropping the TE and leaving an open section.
    npts = 25
    dspan = bladeHeight / nspan

    xUpTwist = [0] * npts
    yUpTwist = [0] * npts
    xLowTwist = [0] * npts
    yLowTwist = [0] * npts
    faces = []
    verts = []

    #Generate Vertices for Unmodified Airfoil Shape
    for j in range(0, nspan + 1):
        x = []
        yThickness = []
        yCamber = []
        xUpper = []
        xLower = []
        yUpper = []
        yLower = []

        m = (1 - j / nspan) * camberRoot + j / nspan * camberTip


        #NACA4Profile
        for i in range(0, npts):
            # Cosine spacing in [0, 1]; i=npts-1 is the trailing edge.
            x.append(1 - cos(i * (pi / 2) / (npts - 1)))
            yThickness.append(thickness / 0.2 * (0.2969 * pow(x[i], 0.5) - 0.126 * x[i] - 0.3516 * pow(x[i], 2) + 0.2843 * pow(x[i], 3) - 0.1015 * pow(x[i], 4)))

            if (x[i] < camberPos):
                yCamber.append(m / pow(camberPos, 2) * (2 * camberPos * x[i] - pow(x[i], 2)))
                dycdx = 2 * m / pow(camberPos, 2) * (camberPos - x[i])

            else:
                yCamber.append(m / pow(1 - camberPos, 2) * (1 - 2 * camberPos + 2 * camberPos * x[i] - pow(x[i], 2)))
                dycdx = 2 * m / pow(1 - camberPos, 2) * (camberPos - x[i])

            x[i] -= cot[0]
            yCamber[i] -= cot[1]

            #Upper and Lower Vertices
            xUpper.append(x[i] - yThickness[i] * (sin(atan(dycdx))))
            yUpper.append(yCamber[i] + yThickness[i] * (cos(atan(dycdx))))
            xLower.append(x[i] + yThickness[i] * (sin(atan(dycdx))))
            yLower.append(yCamber[i] - yThickness[i] * (cos(atan(dycdx))))

        #Generate Vertices Following Twist
        angle = twist * j * dspan
        chord = rootChord - j * dspan * (rootChord - tipChord) / bladeHeight

        for i in range(0, npts):
            xUpTwist[i] = (xUpper[i] * cos(angle) - yUpper[i] * sin(angle)) * chord
            yUpTwist[i] = (xUpper[i] * sin(angle) + yUpper[i] * cos(angle)) * chord

            verts.append([xUpTwist[i], yUpTwist[i], j * dspan])

        for i in range(0, npts):

            xLowTwist[i] = (xLower[i] * cos(angle) - yLower[i] * sin(angle)) * chord
            yLowTwist[i] = (xLower[i] * sin(angle) + yLower[i] * cos(angle)) * chord


            verts.append([xLowTwist[i], yLowTwist[i], j * dspan])

    #Bottom Prof
    faces.append([0, 1, npts + 1])
    for i in range(0, npts - 1):
        faces.append([i, i + 1, npts + i + 1])
        faces.append([i, npts + i + 1, npts + i])

    #Sides
    nPerStage = npts * 2
    for j in range(0, nspan):
        for i in range(0, npts - 1):
            faces.append([nPerStage * j + i, nPerStage * (j + 1) + i, nPerStage * (j + 1) + i + 1])
            faces.append([nPerStage * j + i, nPerStage * (j + 1) + i + 1, nPerStage * j + i + 1])

        for i in range(0, npts - 1):
            faces.append([nPerStage * j + i + npts, nPerStage * (j + 1) + i + 1 + npts, nPerStage * (j + 1) + i + npts])
            faces.append([nPerStage * j + i + npts, nPerStage * j + i + 1 + npts, nPerStage * (j + 1) + i + 1 + npts])
        faces.append([nPerStage * j + npts - 1, nPerStage * (j + 1) + npts - 1, nPerStage * (j + 1) + npts * 2 - 1])
        faces.append([nPerStage * j + npts - 1, nPerStage * (j + 1) + npts * 2 - 1, nPerStage * j + npts * 2 - 1])

    #Top Prof
    faces.append([nPerStage * nspan, nPerStage * nspan + 1, nPerStage * nspan + npts + 1])
    for i in range(0, npts - 1):
        faces.append([nPerStage * nspan + i, nPerStage * nspan + npts + i + 1, nPerStage * nspan + i + 1])
        faces.append([nPerStage * nspan + i, nPerStage * nspan + npts + i, nPerStage * nspan + npts + i + 1])

    return (faces, verts)
    
    
################################
##Function: FindBounds
#Calculates bounding box for given object
##Inputs:
#obj: object to be bounded (mesh)
##Returns:
#minx, maxx, miny, maxy, minz, maxz: (floats)
################################
def FindBounds(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
            
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
            
    return minx, maxx, miny, maxy, minz, maxz

    
################################
##Function: StageProps
#Holds stage angles
##Inputs:
#None
##Returns:
#None
################################
class StageProps():
    def __init__(self):
        self.beta1 = 0
        self.beta2 = 0
        self.alpha1 = 0
        self.alpha2 = 0
        self.cx = 0
        self.rpm = 0
        self.radius = 0
        self.camber = 0
        self.r = 0
        self.phi = 0
        self.psi = 0


################################
##Function: LinearStageProp
#Holds stage properties
##Inputs:
#None
##Returns:
#None
################################
class LinearStageProp():
    def __init__(self):
        # Instance attributes (previously class attributes shared
        # across all instances, leaking state between stages).
        self.rootProps = StageProps()
        self.meanProps = StageProps()
        self.tipProps = StageProps()
        self.rootRadius = 0
        self.tipRadius = 0
    
 
################################
##Function: CalcStageBladeAngles
#Calculates stage angles for the blade
##Inputs:
#r: reaction (float)
#phi: flow (float)
#psi: loading (float)
#rpm: ...rpm (float)
#radius: radius of stage (float)
##Returns:
#stageProps: stage properties (object)
################################ 
def CalcStageBladeAngles(r, phi, psi, rpm, radius):
    # Mean-line velocity triangles. Note beta1 simplifies to
    # atan((2*r + psi) / (2*phi)); kept expanded for traceability.
    # tan(beta2) = (r - psi/2) / phi
    # tan(beta1) = psi/phi + (2*r - psi)/(2*phi)
    if phi == 0:
        raise ValueError("phi must be non-zero")
    if radius <= 0:
        raise ValueError("radius must be > 0")
    u = rpm / 60 * 2 * pi * radius / 1000
    stageProps = StageProps()
    stageProps.rpm = rpm
    stageProps.radius = radius
    stageProps.r = r
    stageProps.phi = phi
    stageProps.psi = psi
    stageProps.beta2 = atan((r - psi / 2) / phi)
    stageProps.beta1 = atan(psi / phi + (2 * r - psi) / (2 * phi))
    stageProps.cx = phi * u
    w1 = stageProps.cx / cos(stageProps.beta1)
    w2 = stageProps.cx / cos(stageProps.beta2)
    c1 = u - w1 * sin(stageProps.beta1)
    c2 = u - w2 * sin(stageProps.beta2)
    if stageProps.cx == 0:
        raise ValueError("axial velocity cx is zero; check phi/rpm/radius")
    stageProps.alpha1 = atan(c1 / stageProps.cx)
    stageProps.alpha2 = atan(c2 / stageProps.cx)

    return stageProps


def camber_from_turning(chord, delta_beta):
    """Camber ratio needed to achieve a given flow turning angle.

    Centralizes the formula previously copy-pasted in BladeRender and
    BladePlot. Guards the sin/tan singularity when turning -> 0.
    """
    import numpy as np
    if chord <= 0:
        raise ValueError("chord must be > 0")
    if abs(float(delta_beta)) < 1e-9:
        return 0.0
    s = float(np.sin(delta_beta))
    t = float(np.tan(delta_beta))
    if abs(s) < 1e-12 or abs(t) < 1e-12:
        return 0.0
    camber = (chord / 2 / s - chord / 2 / t) / chord
    return -1.0 * camber


def _match_cx(r, psi, rpm, radius, target_cx, phi_guess, max_iter=100, tol=1e-3):
    """Bisect local flow coefficient so local cx matches target cx.

    Returns (stageProps, phi). Raises ValueError if not converged,
    instead of looping forever (previously unbounded while loop).
    """
    lphi = 1e-6
    hphi = 2 - 1e-6
    phi = phi_guess
    props = CalcStageBladeAngles(r=r, phi=phi, psi=psi, rpm=rpm, radius=radius)
    for _ in range(max_iter):
        if abs(target_cx - props.cx) <= tol:
            return props, phi
        if props.cx < target_cx:
            lphi = phi
        else:
            hphi = phi
        phi = (hphi + lphi) / 2
        props = CalcStageBladeAngles(r=r, phi=phi, psi=psi, rpm=rpm, radius=radius)
    raise ValueError(
        "StageCalc failed to converge cx (free-vortex match) "
        f"within {max_iter} iterations"
    )
    

################################
##Function: StageCalc
#Calculates propeties of whole stage
##Inputs:
#r: reaction (float)
#phi: flow (float)
#psi: loading (float)
#rpm: ...rpm (float)
#rootRadius: hub radius of stage (float)
#tipRadius: radius of stage (float)
##Returns:
#stageProps: stage properties (object)
################################
def StageCalc(r, phi, psi, rpm, rootRadius, tipRadius):
    if rootRadius <= 0 or tipRadius <= 0:
        raise ValueError("rootRadius and tipRadius must be > 0")
    if tipRadius <= rootRadius:
        raise ValueError("tipRadius must be > rootRadius")
    stageProps = LinearStageProp()
    stageProps.rootRadius = rootRadius
    stageProps.tipRadius = tipRadius

    mlr = (rootRadius + tipRadius) / 2
    stageProps.meanProps = CalcStageBladeAngles(r=r, phi=phi, psi=psi, rpm=rpm, radius=mlr)

    target_cx = stageProps.meanProps.cx

    # Free-vortex: adjust local phi so root/tip cx matches mean cx.
    # The solved phi belongs on root/tip props, NOT on meanProps
    # (previously meanProps.phi was clobbered twice).
    stageProps.rootProps, _rootPhi = _match_cx(
        r, psi, rpm, rootRadius, target_cx, phi)
    stageProps.tipProps, _tipPhi = _match_cx(
        r, psi, rpm, tipRadius, target_cx, phi)

    return stageProps
    